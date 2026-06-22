from typing import Dict, List
from workflow_engine.nodes.base import BaseNode

class LoopNode(BaseNode):
    """循环执行节点"""

    category = "流程控制"
    display_name = "循环"
    node_type = "loop"

    input_ports = [("input", "flow")]
    output_ports = [("output", "flow"), ("done", "flow")]

    config_schema = {
        "items": {"type": "string", "required": True, "description": "迭代列表表达式，如: [1,2,3]"},
        "variable_name": {"type": "string", "default": "item", "description": "循环变量名"},
        "max_iterations": {"type": "int", "default": 1000, "description": "最大迭代次数"}
    }

    def execute(self, inputs: Dict) -> Dict:
        """执行循环"""
        items_expr = self.config.get("items", "[]")
        variable_name = self.config.get("variable_name", "item")
        max_iterations = int(self.config.get("max_iterations", 1000))

        if not items_expr:
            return {"output": [], "done": True, "error": "Empty items expression"}

        try:
            items = self._evaluate_items(items_expr, inputs)
            if not isinstance(items, list):
                return {"output": [], "done": True, "error": "Items must be a list"}

            results = []
            for i, item in enumerate(items):
                if i >= max_iterations:
                    break
                # 设置循环变量到工作流变量
                self.workflow.variables.set(variable_name, item)
                self.workflow.variables.set(f"{variable_name}_index", i)
                results.append({"item": item, "index": i})

            return {
                "output": results,
                "done": True,
                "count": len(results)
            }
        except Exception as e:
            return {"output": [], "done": True, "error": str(e)}

    def _evaluate_items(self, expression: str, context: Dict) -> List:
        """求值列表表达式"""
        local_vars = {}
        var_store = self.workflow.variables.to_dict().get("variables", {})
        local_vars.update(var_store)
        local_vars.update(context)

        try:
            result = eval(expression, {"__builtins__": {}}, local_vars)
            if isinstance(result, list):
                return result
            raise ValueError(f"Expression must return a list, got {type(result)}")
        except Exception as e:
            raise ValueError(f"Items evaluation error: {e}")
