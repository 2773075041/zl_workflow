from typing import Any, Dict, List, Tuple

class BaseNode:
    """节点基类"""
    category: str = ""
    display_name: str = ""
    node_type: str = ""
    input_ports: List[Tuple[str, str]] = []
    output_ports: List[Tuple[str, str]] = []

    def __init__(self, node_id: str, workflow: Any):
        self.node_id = node_id
        self.workflow = workflow
        self.position = {"x": 0, "y": 0}
        self.config = {}
        self._state: str = "idle"

    def set_config(self, config: Dict):
        self.config = config

    def set_state(self, state: str):
        self._state = state

    def get_state(self) -> str:
        return self._state

    def execute(self, inputs: Dict[str, Any]) -> Dict[str, Any]:
        raise NotImplementedError