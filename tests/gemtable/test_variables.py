"""Tests for citrine.informatics.variables."""
import pytest
from gemd.entity.bounds.real_bounds import RealBounds

from citrine.gemtables.variables import *
import citrine.ara.variables as oldvariables
from gemd.entity.link_by_uid import LinkByUID


@pytest.fixture(params=[
    RootInfo(name="root name", headers=["Root", "Name"], field="name"),
    XOR(name="root name or sample_type", headers=["Root", "Info"], variables=[RootInfo(name="root name", headers=["Root", "Name"], field="name"), RootInfo(name="root name", headers=["Root", "Sample Type"], field="sample_type")]),
    AttributeByTemplate(name="density", headers=["density"], template=LinkByUID(scope="templates", id="density"), attribute_constraints=[[LinkByUID(scope="templates", id="density"), RealBounds(0, 100, "g/cm**3")]]),
    AttributeByTemplateAfterProcessTemplate(name="density", headers=["density"], attribute_template=LinkByUID(scope="template", id="density"), process_template=LinkByUID(scope="template", id="process")),
    AttributeByTemplateAndObjectTemplate(name="density", headers=["density"], attribute_template=LinkByUID(scope="template", id="density"), object_template=LinkByUID(scope="template", id="object")),
    AttributeInOutput(name="density", headers=["density"], attribute_template=LinkByUID(scope="template", id="density"), process_templates=[LinkByUID(scope="template", id="object")]),
    IngredientIdentifierByProcessTemplateAndName(name="ingredient id", headers=["density"], process_template=LinkByUID(scope="template", id="process"), ingredient_name="ingredient", scope="scope"),
    IngredientIdentifierInOutput(name="ingredient id", headers=["ingredient id"], ingredient_name="ingredient", process_templates=[LinkByUID(scope="template", id="object")], scope="scope"),
    IngredientLabelByProcessAndName(name="ingredient label", headers=["label"], process_template=LinkByUID(scope="template", id="process"), ingredient_name="ingredient", label="label"),
    IngredientQuantityByProcessAndName(name="ingredient quantity dimension", headers=["quantity"], process_template=LinkByUID(scope="template", id="process"), ingredient_name="ingredient", quantity_dimension=IngredientQuantityDimension.ABSOLUTE),
    IngredientQuantityInOutput(name="ingredient quantity", headers=["ingredient quantity"], ingredient_name="ingredient", quantity_dimension=IngredientQuantityDimension.MASS, process_templates=[LinkByUID(scope="template", id="object")]),
    RootIdentifier(name="root id", headers=["id"], scope="scope")
])
def variable(request):
    return request.param


def test_deser_from_parent(variable):
    # Serialize and deserialize the variables, making sure they are round-trip serializable
    variable_data = variable.dump()
    variable_deserialized = Variable.build(variable_data)
    for attr in variable._attrs():
        variable_attr = getattr(variable, attr)
        variable_deser_attr = getattr(variable_deserialized, attr)
        assert variable_attr == variable_deser_attr
    assert variable == variable_deserialized


def test_invalid_eq(variable):
    other = None
    assert not variable == other


def test_invalid_deser():
    with pytest.raises(ValueError):
        Variable.build({})

    with pytest.raises(ValueError):
        Variable.build({"type": "foo"})


def test_quantity_dimension_serializes_to_string():
    variable = IngredientQuantityByProcessAndName(
        name="ingredient quantity dimension",
        headers=["quantity"],
        process_template=LinkByUID(scope="template", id="process"),
        ingredient_name="ingredient",
        quantity_dimension=IngredientQuantityDimension.NUMBER
    )
    variable_data = variable.dump()
    assert variable_data["quantity_dimension"] == "number"

def test_renamed_classes_are_the_same():
    # Mostly make code coverage happy
    assert oldvariables.IngredientQuantityDimension == IngredientQuantityDimension