from typing import Dict
from workflow_engine.nodes.base import BaseNode

class LLMCallNode(BaseNode):
    """LLM 调用节点"""

    category = "AI"
    display_name = "LLM调用"
    node_type = "llm_call"

    input_ports = [("input", "any")]
    output_ports = [("output", "string")]

    config_schema = {
        "prompt_template": {"type": "string", "required": True, "description": "Prompt 模板，如: Hello {name}!"},
        "model": {"type": "string", "default": "gpt-4", "description": "模型名称"},
        "api_key": {"type": "string", "required": True, "description": "API Key"},
        "temperature": {"type": "float", "default": 0.7, "description": "温度参数"},
        "max_tokens": {"type": "int", "default": 1000, "description": "最大 token 数"}
    }

    def execute(self, inputs: Dict) -> Dict:
        """执行 LLM 调用"""
        prompt_template = self.config.get("prompt_template", "")
        model = self.config.get("model", "gpt-4")
        api_key = self.config.get("api_key", "")
        temperature = float(self.config.get("temperature", 0.7))
        max_tokens = int(self.config.get("max_tokens", 1000))

        if not prompt_template:
            return {"output": None, "error": "Prompt template is required"}

        if not api_key:
            return {"output": None, "error": "API key is required"}

        try:
            rendered_prompt = self._render_template(prompt_template, inputs)
            response = self._call_api(rendered_prompt, model, api_key, temperature, max_tokens)

            return {
                "output": response,
                "model": model,
                "success": True
            }
        except Exception as e:
            return {"output": None, "error": str(e), "success": False}

    def _render_template(self, template: str, context: Dict) -> str:
        """渲染 prompt 模板，使用 {key} 占位符"""
        var_store = self.workflow.variables.to_dict().get("variables", {})
        # inputs 优先级高于工作流变量
        merged_context = {**var_store, **context}

        result = template
        for key, value in merged_context.items():
            placeholder = f"{{{key}}}"
            if placeholder in result:
                result = result.replace(placeholder, str(value))

        return result

    def _call_api(self, prompt: str, model: str, api_key: str, temperature: float, max_tokens: int) -> str:
        """调用 LLM API (占位实现)"""
        # TODO: 实现真实的 OpenAI API 调用
        return f"[Placeholder] LLM response for: {prompt[:50]}..."
