import pytest
from workflow_engine.core.executor import Executor, ExecutionState
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
        return {"result": f"executed {self.node_id}"}

def test_executor_initial_state():
    registry = NodeRegistry()
    registry.register(SimpleNode)

    wf = Workflow()
    wf.add_node("simple", "node1")
    executor = Executor(wf)
    assert executor.state == ExecutionState.IDLE

def test_sequential_execution():
    registry = NodeRegistry()
    registry.register(SimpleNode)

    wf = Workflow()
    wf.add_node("simple", "node1")
    wf.add_node("simple", "node2")
    wf.add_edge("node1", "node2")

    executor = Executor(wf)
    results = executor.execute("sequential")

    assert executor.state == ExecutionState.COMPLETED
    assert "node1" in results
    assert "node2" in results

def test_topological_sort():
    registry = NodeRegistry()
    registry.register(SimpleNode)

    wf = Workflow()
    wf.add_node("simple", "node1")
    wf.add_node("simple", "node2")
    wf.add_node("simple", "node3")
    wf.add_edge("node1", "node2")
    wf.add_edge("node2", "node3")

    executor = Executor(wf)
    order = executor._topological_sort()

    assert order.index("node1") < order.index("node2")
    assert order.index("node2") < order.index("node3")

def test_step_execution():
    registry = NodeRegistry()
    registry.register(SimpleNode)

    wf = Workflow()
    wf.add_node("simple", "node1")
    wf.add_node("simple", "node2")
    wf.add_edge("node1", "node2")

    executor = Executor(wf)

    has_next = executor.step()
    assert executor.current_node_id == "node1"
    assert has_next == True

    has_next = executor.step()
    assert executor.current_node_id == "node2"
    assert has_next == False

def test_get_status():
    registry = NodeRegistry()
    registry.register(SimpleNode)

    wf = Workflow()
    wf.add_node("simple", "node1")

    executor = Executor(wf)
    status = executor.get_status()

    assert status["state"] == "idle"
    assert status["current_node"] is None
    assert status["completed_nodes"] == []