from typing import Dict
from workflow_engine.nodes.base import BaseNode

class ConditionNode(BaseNode):
    """条件分支节点"""

    category = "流程控制"
    display_name = "条件分支"
    node_type = "condition"

    input_ports = [("input", "flow")]
    output_ports = [("true", "flow"), ("false", "flow")]

    config_schema = {
        "expression": {"type": "string", "required": True, "description": "条件表达式，如: x > 10"}
    }

    def execute(self, inputs: Dict) -> Dict:
        """执行条件判断"""
        expression = self.config.get("expression", "")
        if not expression:
            return {"condition": False, "branch": "false", "error": "Empty expression"}

        try:
            result = self._evaluate_expression(expression, inputs)
            return {"condition": result, "branch": "true" if result else "false"}
        except Exception as e:
            return {"condition": False, "branch": "false", "error": str(e)}

    def _evaluate_expression(self, expression: str, context: Dict) -> bool:
        """求值表达式"""
        # 合并变量
        local_vars = {}
        var_store = self.variables.to_dict().get("variables", {})
        local_vars.update(var_store)
        local_vars.update(context)

        try:
            result = eval(expression, {"__builtins__": {}}, local_vars)
            return bool(result)
        except Exception as e:
            raise ValueError(f"Expression evaluation error: {e}")