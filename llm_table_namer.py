import re
from datetime import datetime
from dashscope import Generation
from llm_client import LLMClient

llm = LLMClient(default_model="qwen1.5-32b-chat")

def validate_table_name(name):
    """
    校验MySQL表名是否合法：
    1. 仅小写字母、数字、下划线
    2. 必须字母开头
    3. 长度<=30
    """
    pattern = r'^[a-z][a-z0-9_]{0,29}$'
    return re.match(pattern, name) is not None


def fallback_table_name(filename):
    """
    规则生成表名（备用）
    """
    base = re.sub(r'[^a-zA-Z0-9]', '_', filename.lower())
    if not base[0].isalpha():
        base = "excel_" + base
    return base[:20]


def generate_table_name_by_llm(filename):
    prompt = f"""
你是数据库命名助手。

请根据以下Excel文件名称生成一个MySQL数据表名。

严格要求：
1. 仅使用小写英文字母、数字和下划线
2. 必须以字母开头
3. 不超过30个字符
4. 不要解释
5. 仅输出表名

文件名：
{filename}
"""

    result = llm.call(prompt)

    if not result["success"]:
        return fallback_table_name(filename)

    name = result["content"].replace("```", "").strip()

    if not validate_table_name(name):
        name = fallback_table_name(filename)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    return f"{name}_{timestamp}"