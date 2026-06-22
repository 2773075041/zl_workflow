import pytest
from workflow_engine.core.node_registry import NodeRegistry, BaseNode

class TestNode(BaseNode):
    category = "测试"
    display_name = "测试节点"
    node_type = "test"
    input_ports = [("input", "any")]
    output_ports = [("output", "any")]

    def execute(self, inputs):
        return {"result": "test"}

def test_register_node():
    registry = NodeRegistry()
    registry.register(TestNode)
    assert "test" in registry.get_all_types()

def test_get_node_class():
    registry = NodeRegistry()
    registry.register(TestNode)
    assert registry.get_node_class("test") == TestNode

def test_get_categories():
    registry = NodeRegistry()
    registry.register(TestNode)
    categories = registry.get_categories()
    assert "测试" in categories

def test_get_nodes_by_category():
    registry = NodeRegistry()
    registry.register(TestNode)
    nodes = registry.get_nodes_by_category("测试")
    assert TestNode in nodes

def test_unregister():
    registry = NodeRegistry()
    registry.register(TestNode)
    registry.unregister("test")
    assert "test" not in registry.get_all_types()