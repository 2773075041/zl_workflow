import pytest
from workflow_engine.core.engine import WorkflowEngine
from workflow_engine.core.workflow import Workflow
from workflow_engine.core.node_registry import NodeRegistry
from workflow_engine.nodes.base import BaseNode

class SimpleNode(BaseNode):
    category = "测试"
    display_name = "简单节点"
    node_type = "simple"
    input_ports = [("input", "any")]
    output_ports = [("output", "any")]

    def execute(self, inputs):
        return {"result": f"done"}

def test_add_workflow():
    registry = NodeRegistry()
    registry.register(SimpleNode)

    engine = WorkflowEngine()
    wf = Workflow(name="测试")
    engine.add_workflow(wf)

    assert wf.id in engine.workflows

def test_remove_workflow():
    registry = NodeRegistry()
    registry.register(SimpleNode)

    engine = WorkflowEngine()
    wf = Workflow(name="测试")
    engine.add_workflow(wf)
    engine.remove_workflow(wf.id)

    assert wf.id not in engine.workflows

def test_get_workflow():
    registry = NodeRegistry()
    registry.register(SimpleNode)

    engine = WorkflowEngine()
    wf = Workflow(name="测试")
    engine.add_workflow(wf)

    retrieved = engine.get_workflow(wf.id)
    assert retrieved == wf

def test_run_workflow():
    registry = NodeRegistry()
    registry.register(SimpleNode)

    engine = WorkflowEngine()
    wf = Workflow(name="测试")
    wf.add_node("simple", "node1")
    engine.add_workflow(wf)

    results = engine.run_workflow(wf.id)
    assert "node1" in results

def test_pause_workflow():
    registry = NodeRegistry()
    registry.register(SimpleNode)

    engine = WorkflowEngine()
    wf = Workflow(name="测试")
    wf.add_node("simple", "node1")
    engine.add_workflow(wf)

    engine.run_workflow(wf.id)
    engine.pause_workflow(wf.id)

    status = engine.get_workflow_status(wf.id)
    assert status["state"] == "paused"

def test_stop_workflow():
    registry = NodeRegistry()
    registry.register(SimpleNode)

    engine = WorkflowEngine()
    wf = Workflow(name="测试")
    wf.add_node("simple", "node1")
    engine.add_workflow(wf)

    engine.run_workflow(wf.id)
    engine.stop_workflow(wf.id)

    status = engine.get_workflow_status(wf.id)
    assert status["state"] == "idle"
