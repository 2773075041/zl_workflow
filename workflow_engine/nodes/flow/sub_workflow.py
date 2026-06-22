from typing import Dict, Optional
from workflow_engine.nodes.base import BaseNode
from workflow_engine.core.workflow import Workflow
from workflow_engine.core.executor import Executor

MAX_NESTING_DEPTH = 3


class SubWorkflowNode(BaseNode):
    """子流程节点 - 调用另一个工作流"""

    category = "流程控制"
    display_name = "子流程"
    node_type = "sub_workflow"

    input_ports = [("input", "any")]
    output_ports = [("output", "any")]

    config_schema = {
        "sub_workflow_id": {"type": "string", "required": True, "description": "子工作流ID"},
        "max_depth": {"type": "int", "default": 3, "description": "最大嵌套深度"}
    }

    def __init__(self, node_id: str, workflow: "Workflow"):
        super().__init__(node_id, workflow)
        self._sub_workflow: Optional[Workflow] = None
        self._current_depth = 0

    def set_sub_workflow(self, workflow: Workflow):
        """设置子工作流"""
        self._sub_workflow = workflow

    def execute(self, inputs: Dict) -> Dict:
        """执行子流程"""
        sub_workflow_id = self.config.get("sub_workflow_id", "")
        max_depth = int(self.config.get("max_depth", MAX_NESTING_DEPTH))

        if not sub_workflow_id:
            return {"output": None, "error": "Sub workflow ID not specified"}

        # 检查嵌套深度
        current_depth = getattr(self.workflow, '_subworkflow_depth', 0)
        if current_depth >= max_depth:
            return {"output": None, "error": f"Max nesting depth ({max_depth}) exceeded"}

        if not self._sub_workflow:
            from workflow_engine.storage.workflow_storage import WorkflowStorage
            storage = WorkflowStorage()
            self._sub_workflow = storage.load(sub_workflow_id)

        if not self._sub_workflow:
            return {"output": None, "error": f"Sub workflow '{sub_workflow_id}' not found"}

        try:
            # 设置嵌套深度
            if not hasattr(self.workflow, '_subworkflow_depth'):
                self.workflow._subworkflow_depth = 0
            self.workflow._subworkflow_depth += 1

            executor = Executor(self._sub_workflow)
            results = executor.execute("sequential")

            # 恢复嵌套深度
            self.workflow._subworkflow_depth -= 1

            return {
                "output": results,
                "completed": True
            }
        except Exception as e:
            return {"output": None, "error": str(e)}
