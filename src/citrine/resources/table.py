from typing import Union, Iterable, Optional, Any

import requests

from citrine._rest.collection import Collection
from citrine._rest.paginator import Paginator
from citrine._rest.resource import Resource
from citrine._serialization import properties
from citrine._serialization.properties import UUID
from citrine._session import Session
from citrine._utils.functions import rewrite_s3_links_locally, write_file_locally


class Table(Resource['Table']):
    """A 2-dimensional projection of data.

    (Display) Tables are the basic unit used to flatten and manipulate data objects.
    While data objects can represent complex materials data, the format
    is NOT conducive to analysis and machine learning. Tables, however,
    can be used to 'flatten' data objects into useful projections.

    Attributes
    ----------
    uid: UUID
        Unique uuid4 identifier of this project.
    version: str
        Version number of the Table
    download_url: int
        Url pointing to the location of the Table's contents

    """

    _response_key = 'table'

    uid = properties.Optional(properties.UUID(), 'id')
    version = properties.Optional(properties.Integer, 'version')
    download_url = properties.Optional(properties.String, 'signed_download_url')

    def __init__(self):
        self.uid = None
        self.version = None
        self.download_url = None

    def __str__(self):
        # TODO: Change this to name once that's added to the table model
        return '<Table {!r}, version {}>'.format(self.uid, self.version)

    def read(self, local_path):
        """Read the Table file from S3."""
        # NOTE: this uses the pre-signed S3 download url. If we need to download larger files,
        # we have other options available (using multi-part downloads in parallel , for example).

        data_location = self.download_url
        data_location = rewrite_s3_links_locally(data_location)
        response = requests.get(data_location)
        write_file_locally(response.content, local_path)


class TableCollection(Collection[Table]):
    """Represents the collection of all tables associated with a project."""

    _path_template = 'projects/{project_id}/display-tables'
    _collection_key: str = 'tables'

    def __init__(self, project_id: UUID, session: Session):
        self.project_id = project_id
        self.session: Session = session

    def get(self, uid: Union[UUID, str], version: int) -> Table:
        """Get a Table's metadata."""
        path = self._get_path(uid) + "/versions/{}".format(version)
        data = self.session.get_resource(path)
        return self.build(data)

    def list_versions(self,
                      uid: UUID,
                      page: Optional[int] = None,
                      per_page: int = 100) -> Iterable[Table]:

        class TablePaginator(Paginator[Table]):
            def _extract_unique_identifiers(self, entity: Table) -> Any:
                return (entity.uid, entity.version)

        paginator = TablePaginator()

        def fetch_versions(page: Optional[int], per_page: int) -> Iterable[Table]:
            data = self.session.get_resource(self._get_path() + '/' + str(uid),
                                             params=self._page_params(page, per_page))
            for item in data[self._collection_key]:
                yield self.build(item)

        return paginator.paginate(fetch_versions, page, per_page)

    def build(self, data: dict) -> Table:
        """Build an individual Table from a dictionary."""
        table = Table.build(data)
        table.project_id = self.project_id
        table.session = self.session
        return table

    def register(self, model: Table) -> Table:
        """Tables cannot be created at this time."""
        raise RuntimeError('Creating Tables is not supported at this time.')
