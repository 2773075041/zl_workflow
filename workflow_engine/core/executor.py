from typing import Dict, List, Optional, Any, Callable
from enum import Enum
from collections import defaultdict, deque
from .workflow import Workflow

class ExecutionState(Enum):
    IDLE = "idle"
    RUNNING = "running"
    PAUSED = "paused"
    COMPLETED = "completed"
    FAILED = "failed"

class Executor:
    def __init__(self, workflow: Workflow):
        self.workflow = workflow
        self.state = ExecutionState.IDLE
        self.current_node_id: Optional[str] = None
        self.node_results: Dict[str, Any] = {}
        self.error: Optional[Exception] = None
        self._step_callbacks: List[Callable] = []
        self._order: List[str] = []
        self._current_step_index: int = -1

    def on_step(self, callback: Callable):
        self._step_callbacks.append(callback)

    def execute(self, mode: str = "sequential") -> Dict:
        self.state = ExecutionState.RUNNING
        self.node_results = {}
        self.error = None

        try:
            if mode == "sequential":
                result = self._execute_sequential()
            elif mode == "parallel":
                result = self._execute_parallel()
            else:
                raise ValueError(f"Unknown mode: {mode}")
            self.state = ExecutionState.COMPLETED
            return result
        except Exception as e:
            self.state = ExecutionState.FAILED
            self.error = e
            raise

    def _execute_sequential(self) -> Dict:
        self._order = self._topological_sort()
        for node_id in self._order:
            self.current_node_id = node_id
            node = self.workflow.get_node(node_id)
            if not node:
                continue
            node.set_state("running")
            inputs = self._gather_inputs(node_id)
            result = node.execute(inputs)
            self.node_results[node_id] = result
            node.set_state("completed")
            for cb in self._step_callbacks:
                cb(node_id, result)
        return self.node_results

    def _execute_parallel(self) -> Dict:
        return self._execute_sequential()

    def _topological_sort(self) -> List[str]:
        in_degree = defaultdict(int)
        adj_list = defaultdict(list)

        for node_id in self.workflow.nodes:
            in_degree[node_id] = 0

        for edge in self.workflow.edges:
            source = edge["source"]
            target = edge["target"]
            adj_list[source].append(target)
            in_degree[target] += 1

        queue = deque([node_id for node_id in self.workflow.nodes if in_degree[node_id] == 0])
        result = []

        while queue:
            node_id = queue.popleft()
            result.append(node_id)
            for neighbor in adj_list[node_id]:
                in_degree[neighbor] -= 1
                if in_degree[neighbor] == 0:
                    queue.append(neighbor)

        return result

    def _gather_inputs(self, node_id: str) -> Dict:
        inputs = {}
        for edge in self.workflow.get_incoming_edges(node_id):
            source_result = self.node_results.get(edge["source"], {})
            inputs[edge["source_port"]] = source_result
        return inputs

    def step(self) -> bool:
        if self.state == ExecutionState.IDLE:
            self._order = self._topological_sort()
            if self._order:
                self._current_step_index = 0
                self.current_node_id = self._order[0]
                self.state = ExecutionState.RUNNING
                node = self.workflow.get_node(self.current_node_id)
                if node:
                    node.set_state("running")
                    inputs = self._gather_inputs(self.current_node_id)
                    result = node.execute(inputs)
                    self.node_results[self.current_node_id] = result
                    node.set_state("completed")
                    for cb in self._step_callbacks:
                        cb(self.current_node_id, result)
                return self._current_step_index < len(self._order) - 1
            return False
        elif self.state == ExecutionState.RUNNING:
            self._current_step_index += 1
            if self._current_step_index < len(self._order):
                self.current_node_id = self._order[self._current_step_index]
                node = self.workflow.get_node(self.current_node_id)
                if node:
                    node.set_state("running")
                    inputs = self._gather_inputs(self.current_node_id)
                    result = node.execute(inputs)
                    self.node_results[self.current_node_id] = result
                    node.set_state("completed")
                    for cb in self._step_callbacks:
                        cb(self.current_node_id, result)
                return self._current_step_index < len(self._order) - 1
            else:
                self.state = ExecutionState.COMPLETED
                return False
        return False

    def get_status(self) -> Dict:
        return {
            "state": self.state.value,
            "current_node": self.current_node_id,
            "completed_nodes": list(self.node_results.keys()),
            "error": str(self.error) if self.error else None
        }