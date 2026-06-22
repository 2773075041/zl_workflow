import pytest
from workflow_engine.core.variable_store import VariableStore

def test_set_and_get():
    store = VariableStore()
    store.set("name", "test")
    assert store.get("name") == "test"

def test_get_default():
    store = VariableStore()
    assert store.get("nonexistent", "default") == "default"

def test_typed_variables():
    store = VariableStore()
    store.set("count", 10, int)
    assert store.get_type("count") == int

def test_has():
    store = VariableStore()
    store.set("name", "test")
    assert store.has("name") == True
    assert store.has("nonexistent") == False

def test_remove():
    store = VariableStore()
    store.set("name", "test")
    store.remove("name")
    assert store.has("name") == False

def test_clear():
    store = VariableStore()
    store.set("name", "test")
    store.set("count", 10)
    store.clear()
    assert store.has("name") == False
    assert store.has("count") == False

def test_to_dict():
    store = VariableStore()
    store.set("name", "test")
    store.set("count", 10, int)
    data = store.to_dict()
    assert data["variables"]["name"] == "test"
    assert data["variables"]["count"] == 10
    assert data["types"]["count"] == "int"

def test_from_dict():
    store = VariableStore()
    data = {
        "variables": {"name": "test", "count": 10},
        "types": {"count": "int"}
    }
    store = VariableStore.from_dict(data)
    assert store.get("name") == "test"
    assert store.get("count") == 10
