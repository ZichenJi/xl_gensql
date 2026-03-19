import os
import time
import dashscope
from dashscope import Generation


class LLMClient:
    """
    统一大模型调用封装类
    """

    def __init__(self, default_model="qwen3.5-plus"):
        """
        从环境变量读取 API Key
        """
        api_key = os.getenv("DASHSCOPE_API_KEY")

        if not api_key:
            raise ValueError("未检测到 DASHSCOPE_API_KEY 环境变量")

        dashscope.api_key = api_key
        self.default_model = default_model

    def call(self, prompt, model=None):
        model_name = model if model else self.default_model

        start_time = time.time()

        try:
            response = Generation.call(
                model=model_name,
                messages=[{"role": "user", "content": prompt}],
                result_format="message"
            )

            duration = round(time.time() - start_time, 3)

            if response.status_code == 200:
                content = response.output.choices[0].message.content.strip()

                return {
                    "success": True,
                    "content": content,
                    "time": duration,
                    "input_tokens": response.usage.input_tokens,
                    "output_tokens": response.usage.output_tokens
                }

            else:
                return {
                    "success": False,
                    "error": response.message,
                    "time": duration
                }

        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "time": 0
            }