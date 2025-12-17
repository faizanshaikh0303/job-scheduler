
from typing import Callable, Dict

JOB_REGISTRY: Dict[str, Callable] = {}


def register_job(name: str):
    def decorator(func: Callable):
        JOB_REGISTRY[name] = func
        return func
    return decorator


def get_job(name: str) -> Callable:
    if name not in JOB_REGISTRY:
        raise ValueError(f"Job '{name}' not registered")
    return JOB_REGISTRY[name]

@register_job("print_message")
def print_message(payload: dict):
    print(f"[JOB] Message: {payload['message']}")
