from typing import Dict, List, Any, Optional, TYPE_CHECKING
from abc import ABC, abstractmethod

if TYPE_CHECKING:
    from workflow_engine.core.workflow import Workflow

class BaseNode(ABC):
    """所有节点的基类"""

    category: str = "基础"
    display_name: str = "节点"
    node_type: str = "base"
    input_ports: List[tuple] = []
    output_ports: List[tuple] = []
    config_schema: Dict = {}

    def __init__(self, node_id: str, workflow: "Workflow"):
        self.node_id = node_id
        self.workflow = workflow
        self.config: Dict = {}
        self._state = "pending"

    @abstractmethod
    def execute(self, inputs: Dict) -> Dict:
        """节点执行逻辑，子类必须实现"""
        raise NotImplementedError

    def validate(self) -> bool:
        """节点配置校验"""
        return True

    def set_config(self, config: Dict):
        self.config = config

    def get_state(self) -> str:
        return self._state

    def set_state(self, state: str):
        self._state = state

    @property
    def inputs(self) -> List[str]:
        return [port[0] for port in self.input_ports]

    @property
    def outputs(self) -> List[str]:
        return [port[0] for port in self.output_ports]

    def execute_with_error_handling(self, inputs: Dict) -> Dict:
        """带错误处理的执行"""
        retry_count = int(self.config.get("retry_count", 0))
        fallback_node_id = self.config.get("fallback_node")

        last_error = None
        for attempt in range(retry_count + 1):
            try:
                return self.execute(inputs)
            except Exception as e:
                last_error = e
                if attempt < retry_count:
                    # 重试
                    continue
                # 尝试 fallback
                if fallback_node_id:
                    return self._execute_fallback(fallback_node_id, inputs)
                # 重试次数用完且无 fallback，抛出异常
                raise

        return {"error": str(last_error)}

    def _execute_fallback(self, fallback_node_id: str, inputs: Dict) -> Dict:
        """执行 fallback 节点"""
        fallback_node = self.workflow.get_node(fallback_node_id)
        if fallback_node:
            try:
                return fallback_node.execute(inputs)
            except Exception as e:
                return {"error": f"Fallback failed: {str(e)}"}
        return {"error": f"Fallback node '{fallback_node_id}' not found"}

    def get_error_info(self) -> Dict:
        """获取错误信息"""
        return {
            "node_id": self.node_id,
            "node_type": self.node_type,
            "state": self._state
        }
