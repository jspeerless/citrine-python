# This contains factories for creating test input, using factory boy
# https://factoryboy.readthedocs.io/en/latest/index.html

# Naming convention here is to use "*DataFactory" for dictionaries used as API input/out, and
# <ModelName>Factory for the domain objects themselves

import factory
from taurus.entity.link_by_uid import LinkByUID

from citrine.resources.dataset import Dataset
from citrine.resources.material_run import MaterialRun


class ProjectDataFactory(factory.DictFactory):
    uid = factory.Faker('uuid4')
    name = factory.Faker('company')
    description = factory.Faker('catch_phrase')
    status = 'CREATED'
    created_at = None


class DatasetDataFactory(factory.DictFactory):
    uid = factory.Faker('uuid4')
    name = factory.Faker('company')
    summary = factory.Faker('catch_phrase')
    description = factory.Faker('bs')
    deleted = False
    created_by = factory.Faker('uuid4')
    updated_by = factory.Faker('uuid4')
    deleted_by = factory.Faker('uuid4')
    create_time = None
    update_time = None
    delete_time = None


class IDDataFactory(factory.DictFactory):
    id = factory.Faker('uuid4')


class LinkByUIDInputFactory(factory.DictFactory):
    id = factory.Faker('uuid4')
    type = 'link_by_uid'
    scope = 'id'


class MaterialRunDataFactory(factory.DictFactory):
    uids = factory.SubFactory(IDDataFactory)
    name = factory.Faker('color_name')
    tags = []
    notes = None
    process = factory.SubFactory(LinkByUIDInputFactory)
    sample_type = 'experimental'
    spec = None
    file_links = []
    type = 'material_run'


class LinkByUIDFactory(factory.Factory):
    class Meta:
        model = LinkByUID

    scope = 'id'
    id = factory.Faker('uuid4')


class MaterialRunFactory(factory.Factory):
    class Meta:
        model = MaterialRun

    uids = factory.SubFactory(IDDataFactory)
    name = factory.Faker('color_name')
    tags = []
    notes = None
    process = factory.SubFactory(LinkByUIDFactory)
    sample_type = 'experimental'
    spec = None
    file_links = []


class DatasetFactory(factory.Factory):
    class Meta:
        model = Dataset

    name = factory.Faker('company')
    summary = factory.Faker('catch_phrase')
    description = factory.Faker('bs')