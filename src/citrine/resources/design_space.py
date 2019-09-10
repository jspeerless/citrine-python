"""Resources that represent both collections of design spaces."""
from uuid import UUID
from typing import TypeVar

from citrine._rest.collection import Collection
from citrine._session import Session
from citrine.informatics.design_spaces import DesignSpace

CreationType = TypeVar('CreationType', bound=DesignSpace)


class DesignSpaceCollection(Collection[DesignSpace]):
    """Represents the collection of all design spaces as well as the resources belonging to it."""

    _path_template = '/projects/{project_id}/modules'
    _collection_key = 'entries'
    _individual_key = None
    _resource = DesignSpace

    def __init__(self, project_id: UUID, session: Session = Session()):
        self.project_id = project_id
        self.session: Session = session

    def build(self, data: dict) -> DesignSpace:
        """Build an individual design space."""
        design_space = DesignSpace.build(data)
        design_space.session = self.session
        return design_space

    def register(self, model: CreationType) -> CreationType:
        """Registers a design space."""
        return super().register(model)
