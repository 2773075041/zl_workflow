from typing import Dict, List, Optional, Any
from uuid import uuid4
from .variable_store import VariableStore
from .node_registry import NodeRegistry

class Workflow:
    def __init__(self, workflow_id: Optional[str] = None, name: str = "未命名工作流"):
        self.id = workflow_id or str(uuid4())
        self.name = name
        self.nodes: Dict[str, Any] = {}
        self.edges: List[Dict] = []
        self.variables = VariableStore()
        self._registry = NodeRegistry()

    def add_node(self, node_type: str, node_id: Optional[str] = None, position: Dict = None) -> Any:
        node_id = node_id or f"{node_type}_{len(self.nodes)}"
        node_class = self._registry.get_node_class(node_type)
        if not node_class:
            raise ValueError(f"Node type '{node_type}' not registered")
        node = node_class(node_id, self)
        node.position = position or {"x": 0, "y": 0}
        self.nodes[node_id] = node
        return node

    def remove_node(self, node_id: str):
        self.nodes.pop(node_id, None)
        self.edges = [e for e in self.edges if e["source"] != node_id and e["target"] != node_id]

    def add_edge(self, source: str, target: str, source_port: str = "output", target_port: str = "input"):
        self.edges.append({
            "source": source,
            "target": target,
            "source_port": source_port,
            "target_port": target_port
        })

    def remove_edge(self, source: str, target: str):
        self.edges = [e for e in self.edges if not (e["source"] == source and e["target"] == target)]

    def get_node(self, node_id: str) -> Optional[Any]:
        return self.nodes.get(node_id)

    def get_outgoing_edges(self, node_id: str) -> List[Dict]:
        return [e for e in self.edges if e["source"] == node_id]

    def get_incoming_edges(self, node_id: str) -> List[Dict]:
        return [e for e in self.edges if e["target"] == node_id]

    def to_dict(self) -> Dict:
        return {
            "id": self.id,
            "name": self.name,
            "nodes": [
                {
                    "id": node_id,
                    "type": node.node_type,
                    "category": node.category,
                    "position": getattr(node, "position", {"x": 0, "y": 0}),
                    "config": getattr(node, "config", {})
                }
                for node_id, node in self.nodes.items()
            ],
            "edges": self.edges,
            "variables": self.variables.to_dict()
        }

    @classmethod
    def from_dict(cls, data: Dict) -> "Workflow":
        workflow = cls(workflow_id=data["id"], name=data["name"])
        workflow.edges = data.get("edges", [])
        workflow.variables = VariableStore.from_dict(data.get("variables", {}))
        for node_data in data.get("nodes", []):
            node = workflow.add_node(node_data["type"], node_data["id"], node_data.get("position"))
            node.set_config(node_data.get("config", {}))
        return workflow
