from typing import Dict, List, Optional
from workflow_engine.nodes.base import BaseNode

class AgentNode(BaseNode):
    """AI Agent 节点"""

    category = "AI"
    display_name = "AI Agent"
    node_type = "agent"

    input_ports = [("input", "any")]
    output_ports = [("output", "any")]

    config_schema = {
        "prompt": {"type": "string", "required": True, "description": "Agent 提示词"},
        "model": {"type": "string", "default": "gpt-4", "description": "模型名称"},
        "api_key": {"type": "string", "required": True, "description": "API Key"},
        "tools": {"type": "list", "default": [], "description": "可用工具列表"},
        "temperature": {"type": "float", "default": 0.7, "description": "温度参数"}
    }

    def execute(self, inputs: Dict) -> Dict:
        """执行 Agent"""
        prompt = self.config.get("prompt", "")
        model = self.config.get("model", "gpt-4")
        api_key = self.config.get("api_key", "")
        temperature = float(self.config.get("temperature", 0.7))

        if not prompt:
            return {"output": None, "error": "Prompt is required"}

        if not api_key:
            return {"output": None, "error": "API key is required"}

        try:
            response = self._call_llm(prompt, model, api_key, temperature, inputs)
            return {
                "output": response,
                "model": model,
                "success": True
            }
        except Exception as e:
            return {"output": None, "error": str(e), "success": False}

    def _call_llm(self, prompt: str, model: str, api_key: str, temperature: float, context: Dict) -> str:
        """调用 LLM API
        
        这是一个占位实现，实际使用时需要替换为真实的 OpenAI API 调用
        """
        # 构建完整提示词
        full_prompt = self._build_prompt(prompt, context)

        # TODO: 实现真实的 OpenAI API 调用
        # 示例:
        # from openai import OpenAI
        # client = OpenAI(api_key=api_key)
        # response = client.chat.completions.create(
        #     model=model,
        #     messages=[{"role": "user", "content": full_prompt}],
        #     temperature=temperature
        # )
        # return response.choices[0].message.content

        return f"[Placeholder] LLM response for: {full_prompt[:100]}..."

    def _build_prompt(self, prompt: str, context: Dict) -> str:
        """构建完整提示词"""
        # 合并工作流变量
        var_store = self.workflow.variables.to_dict().get("variables", {})
        context_str = "\n".join([f"{k}: {v}" for k, v in var_store.items()])

        full_prompt = prompt
        if context_str:
            full_prompt += f"\n\nContext:\n{context_str}"

        return full_prompt
