from typing import Dict, Optional
from .workflow import Workflow
from .executor import Executor, ExecutionState

class WorkflowEngine:
    """工作流引擎 - 管理所有工作流"""

    def __init__(self):
        self.workflows: Dict[str, Workflow] = {}
        self.active_executors: Dict[str, Executor] = {}

    def add_workflow(self, workflow: Workflow):
        """添加工作流"""
        self.workflows[workflow.id] = workflow

    def remove_workflow(self, workflow_id: str):
        """移除工作流"""
        self.workflows.pop(workflow_id, None)
        self.active_executors.pop(workflow_id, None)

    def get_workflow(self, workflow_id: str) -> Optional[Workflow]:
        """获取工作流"""
        return self.workflows.get(workflow_id)

    def list_workflows(self):
        """列出所有工作流"""
        return list(self.workflows.keys())

    def run_workflow(self, workflow_id: str, mode: str = "sequential") -> Dict:
        """运行工作流"""
        workflow = self.get_workflow(workflow_id)
        if not workflow:
            raise ValueError(f"Workflow {workflow_id} not found")
        executor = Executor(workflow)
        self.active_executors[workflow_id] = executor
        return executor.execute(mode)

    def pause_workflow(self, workflow_id: str):
        """暂停工作流"""
        executor = self.active_executors.get(workflow_id)
        if executor:
            executor.state = ExecutionState.PAUSED

    def stop_workflow(self, workflow_id: str):
        """停止工作流"""
        executor = self.active_executors.get(workflow_id)
        if executor:
            executor.state = ExecutionState.IDLE

    def get_workflow_status(self, workflow_id: str) -> Optional[Dict]:
        """获取工作流状态"""
        executor = self.active_executors.get(workflow_id)
        return executor.get_status() if executor else None

    def is_workflow_running(self, workflow_id: str) -> bool:
        """检查工作流是否在运行"""
        executor = self.active_executors.get(workflow_id)
        return executor.state == ExecutionState.RUNNING if executor else False
