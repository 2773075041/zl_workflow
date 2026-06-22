from typing import Any, Dict, Optional

class VariableStore:
    """工作流级变量存储"""

    def __init__(self):
        self._variables: Dict[str, Any] = {}
        self._types: Dict[str, type] = {}

    def set(self, key: str, value: Any, vtype: Optional[type] = None):
        self._variables[key] = value
        if vtype:
            self._types[key] = vtype

    def get(self, key: str, default: Any = None) -> Any:
        return self._variables.get(key, default)

    def get_type(self, key: str) -> type:
        return self._types.get(key, type(self._variables.get(key)))

    def has(self, key: str) -> bool:
        return key in self._variables

    def remove(self, key: str):
        self._variables.pop(key, None)
        self._types.pop(key, None)

    def clear(self):
        self._variables.clear()
        self._types.clear()

    def to_dict(self) -> Dict:
        return {
            "variables": self._variables,
            "types": {k: v.__name__ for k, v in self._types.items()}
        }

    @classmethod
    def from_dict(cls, data: Dict) -> "VariableStore":
        store = cls()
        store._variables = data.get("variables", {})
        return store
