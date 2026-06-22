from typing import Dict, List, Type, Optional
from workflow_engine.nodes.base import BaseNode

class NodeRegistry:
    """节点注册表"""

    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._nodes = {}
        return cls._instance

    def __init__(self):
        if not hasattr(self, '_nodes'):
            self._nodes: Dict[str, Type[BaseNode]] = {}

    def register(self, node_class: Type[BaseNode]):
        """注册节点类"""
        self._nodes[node_class.node_type] = node_class

    def unregister(self, node_type: str):
        """取消注册"""
        self._nodes.pop(node_type, None)

    def get_node_class(self, node_type: str) -> Optional[Type[BaseNode]]:
        """获取节点类"""
        return self._nodes.get(node_type)

    def get_all_types(self) -> List[str]:
        """获取所有节点类型"""
        return list(self._nodes.keys())

    def get_categories(self) -> List[str]:
        """获取所有分类"""
        categories = set()
        for node_class in self._nodes.values():
            categories.add(node_class.category)
        return list(categories)

    def get_nodes_by_category(self, category: str) -> List[Type[BaseNode]]:
        """按分类获取节点"""
        return [
            node_class for node_class in self._nodes.values()
            if node_class.category == category
        ]

    def clear(self):
        """清空注册表"""
        self._nodes.clear()