from llm_xml_parser import parse_llm_xml
from typing import Callable, Any, List, Dict, Optional, Literal
import os


def create_openrouter_inference(
    task_type_name: Literal[
        "SMF","CMO", "CMI" "Any"
    ],
    model: str = "openai/gpt-5", #  "openai/gpt-5", "openai/o4-mini-high","google/gemini-2.5-flash", "google/gemma-3-27b-it","qwen/qwen2.5-vl-72b-instruct","qwen/qwen-vl-max","qwen/qwen2.5-vl-72b-instruct"
    # json_object_limit: bool = False,
    api_key: Optional[str] = os.environ["OPENROUTER_API_KEY"],
    base_url: Optional[str] = "https://openrouter.ai/api/v1",
    temperature: float = 0,
) -> Callable:
    """
    创建默认的 OpenRouter 推理函数

    Args:
        task_type_name: 任务类型名称，支持 "SMO", "CMO", "CMI", "Any"
        model: 模型名称，默认为 "openai/gpt-5"
        json_object_limit: 是否使用json_objecr对象限制方式，默认不使用，而是使用schema模式
        api_key: OpenAI API密钥，默认从环境变量读取
        base_url: API基础URL，默认使用openrouter.ai

    Returns:
        推理函数，接收messages参数，返回响应对象
    """
    try:
        from openai import OpenAI
    except ImportError:
        raise ImportError("Not found openai: pip install openai")
    # 动态加载模型结构
    from . import pydantic_defination

    try:
        model_class = getattr(pydantic_defination, task_type_name)
    except AttributeError:
        raise ValueError(f"Not found model_class: {task_type_name}")

    # 控制json输出格式
    # if json_object_limit:
    #     response_format = {"type": "json_object"}
    # else:
    #     response_format = {
    #         "type": "json_schema",
    #         "name": model_class.__name__,
    #         "schema": model_class.model_json_schema(),
    #         "strict": True,
    #     }

    # Client初始化
    client_kwargs = {}
    if api_key is not None:
        client_kwargs["api_key"] = api_key
    if base_url is not None:
        client_kwargs["base_url"] = base_url
    client = OpenAI(**client_kwargs)

    def inference_func(messages: List[Dict]) -> Any:
        """
        调用 OpenAI API 进行推理

        Args:
            messages: 消息列表
            [
                {
                    "role": "system",
                    "content": system_prompt
                },
                {
                    "role": "user",
                    "content": user_prompt
                }
            ]

        Returns:
            推理结果(已经序列化过的)
        """
        response = client.chat.completions.create(
            model=model,
            messages=messages,
            temperature=temperature,
        )
        return parse_llm_xml(response.choices[0].message.content)

    return inference_func
