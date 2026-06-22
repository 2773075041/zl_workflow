from typing import Any, Dict, List, Tuple

class BaseNode:
    """节点基类"""
    category: str = ""
    display_name: str = ""
    node_type: str = ""
    input_ports: List[Tuple[str, str]] = []
    output_ports: List[Tuple[str, str]] = []

    def execute(self, inputs: Dict[str, Any]) -> Dict[str, Any]:
        raise NotImplementedError