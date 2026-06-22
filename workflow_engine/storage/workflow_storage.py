import json
import os
from typing import Optional, List
from workflow_engine.core.workflow import Workflow


class WorkflowStorage:
    """工作流存储 - JSON 文件存储"""

    def __init__(self, storage_dir: str = "workflows"):
        self.storage_dir = storage_dir
        os.makedirs(storage_dir, exist_ok=True)

    def save(self, workflow: Workflow) -> str:
        """保存工作流到文件"""
        filepath = os.path.join(self.storage_dir, f"{workflow.id}.json")
        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(workflow.to_dict(), f, ensure_ascii=False, indent=2)
        return filepath

    def load(self, workflow_id: str) -> Optional[Workflow]:
        """从文件加载工作流"""
        filepath = os.path.join(self.storage_dir, f"{workflow_id}.json")
        if not os.path.exists(filepath):
            return None
        with open(filepath, "r", encoding="utf-8") as f:
            data = json.load(f)
        return Workflow.from_dict(data)

    def list_workflows(self) -> List[dict]:
        """列出所有工作流"""
        workflows = []
        if not os.path.exists(self.storage_dir):
            return workflows
        for filename in os.listdir(self.storage_dir):
            if filename.endswith(".json"):
                filepath = os.path.join(self.storage_dir, filename)
                try:
                    with open(filepath, "r", encoding="utf-8") as f:
                        data = json.load(f)
                        workflows.append({
                            "id": data.get("id"),
                            "name": data.get("name", "未命名"),
                            "node_count": len(data.get("nodes", []))
                        })
                except:
                    pass
        return workflows

    def delete(self, workflow_id: str) -> bool:
        """删除工作流"""
        filepath = os.path.join(self.storage_dir, f"{workflow_id}.json")
        if os.path.exists(filepath):
            os.remove(filepath)
            return True
        return False

    def exists(self, workflow_id: str) -> bool:
        """检查工作流是否存在"""
        filepath = os.path.join(self.storage_dir, f"{workflow_id}.json")
        return os.path.exists(filepath)
