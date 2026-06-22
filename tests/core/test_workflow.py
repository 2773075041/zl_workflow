import pytest
from workflow_engine.core.workflow import Workflow
from workflow_engine.core.node_registry import NodeRegistry

class DummyNode:
    category = "测试"
    display_name = "测试节点"
    node_type = "dummy"
    input_ports = [("input", "any")]
    output_ports = [("output", "any")]

    def __init__(self, node_id, workflow):
        self.node_id = node_id
        self.workflow = workflow
        self.position = {"x": 0, "y": 0}
        self.config = {}

    def set_config(self, config):
        self.config = config

    def execute(self, inputs):
        return {"result": "done"}

def test_create_workflow():
    wf = Workflow(name="测试工作流")
    assert wf.name == "测试工作流"
    assert len(wf.nodes) == 0
    assert len(wf.edges) == 0

def test_add_node():
    registry = NodeRegistry()
    registry.register(DummyNode)

    wf = Workflow()
    node = wf.add_node("dummy", "node1")
    assert node.node_id == "node1"
    assert "node1" in wf.nodes

def test_remove_node():
    registry = NodeRegistry()
    registry.register(DummyNode)

    wf = Workflow()
    wf.add_node("dummy", "node1")
    wf.remove_node("node1")
    assert "node1" not in wf.nodes

def test_add_edge():
    registry = NodeRegistry()
    registry.register(DummyNode)

    wf = Workflow()
    wf.add_node("dummy", "node1")
    wf.add_node("dummy", "node2")
    wf.add_edge("node1", "node2")
    assert len(wf.edges) == 1
    assert wf.edges[0]["source"] == "node1"
    assert wf.edges[0]["target"] == "node2"

def test_remove_edge():
    registry = NodeRegistry()
    registry.register(DummyNode)

    wf = Workflow()
    wf.add_node("dummy", "node1")
    wf.add_node("dummy", "node2")
    wf.add_edge("node1", "node2")
    wf.remove_edge("node1", "node2")
    assert len(wf.edges) == 0

def test_to_dict():
    registry = NodeRegistry()
    registry.register(DummyNode)

    wf = Workflow(name="测试")
    wf.add_node("dummy", "node1")
    wf.add_node("dummy", "node2")
    wf.add_edge("node1", "node2")

    data = wf.to_dict()
    assert data["name"] == "测试"
    assert len(data["nodes"]) == 2
    assert len(data["edges"]) == 1

def test_from_dict():
    registry = NodeRegistry()
    registry.register(DummyNode)

    data = {
        "id": "test-id",
        "name": "测试",
        "nodes": [
            {"id": "node1", "type": "dummy", "category": "测试", "position": {"x": 0, "y": 0}, "config": {}}
        ],
        "edges": [],
        "variables": {"variables": {}, "types": {}}
    }
    wf = Workflow.from_dict(data)
    assert wf.name == "测试"
    assert "node1" in wf.nodes
