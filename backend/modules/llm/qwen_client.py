"""
Minimal OpenAI-compatible client for DashScope Qwen (API)endpoints.
把底层 HTTP 调用和异常处理封装起来，对外只暴露一个 generate 方法，方便服务层调用
"""

# 使用 Python 3.7+ 中引入的一个未来特性导入，用于推迟类型注解的求值
# 使用该依赖库，所有类型注解都不会立即被解释为类型对象，而是作为字符串存储，直到真正需要时再解析
# - 可以让类型注解里引用还没定义的类（比如类自身或后面才定义的类），避免循环引用或顺序问题。
# - 还能减少运行时的类型检查开销，加快模块加载速度
from __future__ import annotations

import logging
from typing import Any, Dict

# Python 中常用的 HTTP 客户端库，用于发送网络请求
# - requests.post(url, json=..., headers=...) 可以直接发送 JSON 格式的 POST 请求
import requests

# 使用 Python 标准库 logging 来获取一个和当前模块同名的日志记录器
# - __name__ 是当前模块的名字（如 'backend.modules.llm.qwen_client'）
# - 日志输出时能显示是该模块（'backend.modules.llm.qwen_client'）产生的日志
# - 便于在大型项目中区分不同模块的日志来源
logger = logging.getLogger(__name__)

class QwenClient:
    """Thin wrapper around the DashScope OpenAI-compatible chat endpoint.
    实现了一个面向 DashScope 通义千问 Qwen 大模型 API 的轻量级客户端，其接口风格兼容 OpenAI 的 chat/completions API
    它的主要作用是：
        - 封装与大模型 API 的 HTTP 通信细节
        - 统一异常处理
        - 对外只暴露 generate 方法，便于服务层调用
    """

    def __init__(
        self,
        api_key: str,
        base_url: str,
        default_model: str,
        temperature: float = 0.7,
        max_tokens: int = 1000,
    ) -> None:
        self.api_key = api_key                  # API 密钥，用于身份验证
        self.base_url = base_url.rstrip("/")    # API 基础 URL，去除末尾斜杠以防重复
        self.default_model = default_model      # 默认使用的大模型名称
        self.temperature = temperature          # 生成文本的随机性参数
        self.max_tokens = max_tokens            # 生成文本的最大长度

    def generate(self, prompt: str, *, model: str | None = None) -> str:
        """
        Send a chat completion request and return the assistant message text.
        The standard OpenAI Chat API protocol is adopted for compatibility and scalability.
        All exceptions are caught and converted into unified Python errors, 
            facilitating handling by the service layer and upper-level callers.
        Args:
            prompt: The user input text to send to the model.
            model: Optional model name to override the default.(Optional)
        Returns:
            The generated assistant reply text from the model.
        """

        # 需要发送给大模型 API 的请求体（JSON 格式）
        # - OpenAI Chat API 采用“消息列表”格式，每条消息有 role（system/user/assistant）和 content（文本内容）
        # - temperature 控制生成的多样性，max_tokens 控制回复长度
        payload: Dict[str, Any] = {
            "model": model or self.default_model, # Use specified model or default
            "messages": [
                {
                    # 系统提示，设定 AI 的角色和风格
                    "role": "system",
                    "content": "You are InnerEcho, a friendly and concise listener.",
                },
                {   "role": "user", 
                    "content": prompt
                },
            ],
            "temperature": self.temperature,    # 生成文本的随机性，值越大回复越有创造性（随机）
            "max_tokens": self.max_tokens,      # 回复的最大长度（token 数）
        }
        
        # 设置 HTTP 请求头，包含授权信息和内容类型    
        headers = {
            # "Authorization"：带上 Bearer Token（API 密钥），用于身份验证
            # - Bearer Token 是常见的 API 鉴权方式
            "Authorization": f"Bearer {self.api_key}",
            # "Content-Type"：声明请求体为 JSON 格式
            # - RESTful API 通常用 Content-Type: application/json 来表示请求体是 JSON 数据
            "Content-Type": "application/json",
        }

        # 构造完整的 API 请求 URL
        # 完整 URL 示例参考: https://bailian.console.aliyun.com/cn-beijing/?tab=api#/api/?type=model&url=2833609
        url = f"{self.base_url}/chat/completions"

        # 发送请求与异常处理
        try:
            # 用 requests.post 发送 POST 请求
            # - url：请求地址
            # - json=payload：自动将 payload 转为 JSON 格式并放入请求体
            # - headers：请求头。
            # - timeout=30：最多等待 30 秒
            response = requests.post(url, json=payload, headers=headers, timeout=30)
        except requests.RequestException as exc:  # Network/timeout errors
            # 如果网络异常（如超时、断网），捕获异常，记录日志，并抛出自定义错误
            logger.error("Request to model gateway failed: %s", exc)
            raise RuntimeError("Failed to reach model API") from exc

        # 检查响应状态码
        # - HTTP 状态码 4xx/5xx 表示客户端或服务端错误
        # - 判断返回的状态码是否 >= 400，表示请求失败，记录警告日志并抛出错误
        if response.status_code >= 400:
            logger.warning("Model API error %s: %s", response.status_code, response.text)
            raise RuntimeError(f"Model API error: {response.status_code}")

        # 解析响应体 JSON 数据
        # - 将响应内容解析为 JSON 格式（Python 字典）
        data = response.json()

        # 提取生成的文本内容
        # - OpenAI Chat API 的标准响应结构
        # {
        #   "choices": [
        #     {
        #       "message": {
        #         "role": "assistant",
        #         "content": "模型回复内容"
        #       }
        #     }
        #   ]
        # }
        try:
            # 按照 OpenAI 风格，回复内容在 choices[0]["message"]["content"]
            return data["choices"][0]["message"]["content"]
        except (KeyError, IndexError, TypeError) as exc:
            # 异常处理：如果响应结构不符（如 key 不存在），捕获异常，记录日志，并抛出自定义错误
            logger.error("Unexpected model API response: %s", data)
            raise RuntimeError("Model API response format unexpected") from exc
