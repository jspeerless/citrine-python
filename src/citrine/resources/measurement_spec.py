"""Resources that represent measurement spec data objects."""
from typing import List, Dict, Optional, Type, Union, Iterator
from uuid import UUID

from citrine._rest.resource import Resource
from citrine._serialization.properties import List as PropertyList
from citrine._serialization.properties import Optional as PropertyOptional
from citrine._serialization.properties import String, Object, Mapping, LinkOrElse
from citrine.resources.data_concepts import DataConcepts, CITRINE_SCOPE
from citrine.resources.object_specs import ObjectSpec, ObjectSpecCollection
from gemd.entity.attribute.condition import Condition
from gemd.entity.attribute.parameter import Parameter
from gemd.entity.file_link import FileLink
from gemd.entity.object.measurement_spec import MeasurementSpec as GEMDMeasurementSpec
from gemd.entity.template.measurement_template import \
    MeasurementTemplate as GEMDMeasurementTemplate


class MeasurementSpec(ObjectSpec, Resource['MeasurementSpec'], GEMDMeasurementSpec):
    """
    A measurement specification.

    Parameters
    ----------
    name: str
        Name of the measurement spec.
    uids: Map[str, str], optional
        A collection of
        `unique IDs <https://citrineinformatics.github.io/gemd-docs/
        specification/unique-identifiers/>`_.
    tags: List[str], optional
        `Tags <https://citrineinformatics.github.io/gemd-docs/specification/tags/>`_
        are hierarchical strings that store information about an entity. They can be used
        for filtering and discoverability.
    notes: str, optional
        Long-form notes about the measurement spec.
    conditions: List[Condition], optional
        Conditions under which this measurement spec occurs.
    parameters: List[Parameter], optional
        Parameters of this measurement spec.
    template: MeasurementTemplate
        A template bounding the valid values for the measurement's properties, parameters,
        and conditions.
    file_links: List[FileLink], optional
        Links to associated files, with resource paths into the files API.

    """

    _response_key = GEMDMeasurementSpec.typ  # 'measurement_spec'

    name = String('name')
    uids = Mapping(String('scope'), String('id'), 'uids')
    tags = PropertyOptional(PropertyList(String()), 'tags')
    notes = PropertyOptional(String(), 'notes')
    conditions = PropertyOptional(PropertyList(Object(Condition)), 'conditions')
    parameters = PropertyOptional(PropertyList(Object(Parameter)), 'parameters')
    template = PropertyOptional(LinkOrElse(), 'template')
    file_links = PropertyOptional(PropertyList(Object(FileLink)), 'file_links')
    typ = String('type')

    def __init__(self,
                 name: str,
                 *,
                 uids: Optional[Dict[str, str]] = None,
                 tags: Optional[List[str]] = None,
                 notes: Optional[str] = None,
                 conditions: Optional[List[Condition]] = None,
                 parameters: Optional[List[Parameter]] = None,
                 template: Optional[GEMDMeasurementTemplate] = None,
                 file_links: Optional[List[FileLink]] = None):
        if uids is None:
            uids = dict()
        DataConcepts.__init__(self, GEMDMeasurementSpec.typ)
        GEMDMeasurementSpec.__init__(self, name=name, uids=uids,
                                     tags=tags, conditions=conditions, parameters=parameters,
                                     template=template, file_links=file_links, notes=notes)

    def __str__(self):
        return '<Measurement spec {!r}>'.format(self.name)


class MeasurementSpecCollection(ObjectSpecCollection[MeasurementSpec]):
    """Represents the collection of all measurement specs associated with a dataset."""

    _path_template = 'projects/{project_id}/datasets/{dataset_id}/measurement-specs'
    _dataset_agnostic_path_template = 'projects/{project_id}/measurement-specs'
    _individual_key = 'measurement_spec'
    _collection_key = 'measurement_specs'
    _resource = MeasurementSpec

    @classmethod
    def get_type(cls) -> Type[MeasurementSpec]:
        """Return the resource type in the collection."""
        return MeasurementSpec

    def list_by_template(self, uid: Union[UUID, str],
                         scope: str = CITRINE_SCOPE) -> Iterator[MeasurementSpec]:
        """
        [ALPHA] Get the measurement specs using the specified measurement template.

        Parameters
        ----------
        uid
            The unique ID of the measurement template whose measurement spec usages are
            to be located.
        scope
            The scope of `uid`.
        Returns
        -------
        Iterator[MeasurementSpec]
            The measurement specs using the specified measurement template.

        """
        return self._get_relation('measurement-templates', uid=uid, scope=scope)
