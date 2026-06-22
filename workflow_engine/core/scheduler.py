from typing import Dict, Optional, List
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.interval import IntervalTrigger
from apscheduler.triggers.cron import CronTrigger

class Scheduler:
    """工作流调度器 - 基于 APScheduler"""

    def __init__(self):
        self._scheduler = BackgroundScheduler()
        self._jobs: Dict[str, Dict] = {}
        self._engine = None
        self._history_storage = None

    def set_engine(self, engine):
        """设置工作流引擎引用"""
        self._engine = engine

    def set_history_storage(self, history_storage):
        """设置历史存储引用"""
        self._history_storage = history_storage

    def add_interval_job(self, job_id: str, workflow_id: str, seconds: int):
        """添加间隔任务"""
        def job_wrapper():
            if self._engine:
                execution_id = None
                if self._history_storage:
                    workflow = self._engine.get_workflow(workflow_id)
                    workflow_name = workflow.name if workflow else ""
                    execution_id = self._history_storage.add_execution(workflow_id, workflow_name)
                try:
                    self._engine.run_workflow(workflow_id)
                    if self._history_storage and execution_id:
                        self._history_storage.finish_execution(execution_id, "completed")
                except Exception as e:
                    if self._history_storage and execution_id:
                        self._history_storage.finish_execution(execution_id, "failed", error_message=str(e))

        job = self._scheduler.add_job(
            job_wrapper,
            trigger=IntervalTrigger(seconds=seconds),
            id=job_id,
            replace=True
        )
        self._jobs[job_id] = {
            "type": "interval",
            "workflow_id": workflow_id,
            "interval_seconds": seconds,
            "job_id": job.id
        }

    def add_daily_job(self, job_id: str, workflow_id: str, hour: int, minute: int):
        """添加每日定时任务"""
        def job_wrapper():
            if self._engine:
                execution_id = None
                if self._history_storage:
                    workflow = self._engine.get_workflow(workflow_id)
                    workflow_name = workflow.name if workflow else ""
                    execution_id = self._history_storage.add_execution(workflow_id, workflow_name)
                try:
                    self._engine.run_workflow(workflow_id)
                    if self._history_storage and execution_id:
                        self._history_storage.finish_execution(execution_id, "completed")
                except Exception as e:
                    if self._history_storage and execution_id:
                        self._history_storage.finish_execution(execution_id, "failed", error_message=str(e))

        job = self._scheduler.add_job(
            job_wrapper,
            trigger=CronTrigger(hour=hour, minute=minute),
            id=job_id,
            replace=True
        )
        self._jobs[job_id] = {
            "type": "daily",
            "workflow_id": workflow_id,
            "hour": hour,
            "minute": minute,
            "job_id": job.id
        }

    def add_cron_job(self, job_id: str, workflow_id: str, cron_expr: str):
        """添加 Cron 表达式任务"""
        parts = cron_expr.split()
        if len(parts) != 5:
            raise ValueError("Cron expression must have 5 fields: minute hour day month day_of_week")

        def job_wrapper():
            if self._engine:
                execution_id = None
                if self._history_storage:
                    workflow = self._engine.get_workflow(workflow_id)
                    workflow_name = workflow.name if workflow else ""
                    execution_id = self._history_storage.add_execution(workflow_id, workflow_name)
                try:
                    self._engine.run_workflow(workflow_id)
                    if self._history_storage and execution_id:
                        self._history_storage.finish_execution(execution_id, "completed")
                except Exception as e:
                    if self._history_storage and execution_id:
                        self._history_storage.finish_execution(execution_id, "failed", error_message=str(e))

        trigger = CronTrigger(
            minute=parts[0],
            hour=parts[1],
            day=parts[2],
            month=parts[3],
            day_of_week=parts[4]
        )
        job = self._scheduler.add_job(job_wrapper, trigger=trigger, id=job_id, replace=True)
        self._jobs[job_id] = {
            "type": "cron",
            "workflow_id": workflow_id,
            "cron_expr": cron_expr,
            "job_id": job.id
        }

    def remove_job(self, job_id: str):
        """移除任务"""
        if job_id in self._jobs:
            self._scheduler.remove_job(job_id)
            del self._jobs[job_id]

    def get_jobs(self) -> List[Dict]:
        """获取所有任务"""
        return [
            {
                "id": job_id,
                "type": job["type"],
                "workflow_id": job["workflow_id"]
            }
            for job_id, job in self._jobs.items()
        ]

    def start(self):
        """启动调度器"""
        if not self._scheduler.running:
            self._scheduler.start()

    def stop(self):
        """停止调度器"""
        if self._scheduler.running:
            self._scheduler.shutdown(wait=False)

    def is_running(self) -> bool:
        """检查调度器是否运行"""
        return self._scheduler.running
