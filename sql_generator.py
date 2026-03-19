from llm_client import LLMClient

llm = LLMClient(default_model="qwen1.5-32b-chat")

def validate_sql(sql):
    sql = sql.strip().lower()

    if not sql.startswith("select"):
        return False

    if ";" in sql[:-1]:
        return False

    forbidden = ["drop", "delete", "update", "insert", "alter"]
    for word in forbidden:
        if word in sql:
            return False

    return True

def generate_sql(question, table_name, schema_info):
    prompt = f"""
你是SQL生成助手。

当前数据表：{table_name}

表结构：
{schema_info}

要求：
1. 仅生成SELECT语句
2. 不允许解释
3. 不允许使用不存在字段
4. 不允许多语句

用户问题：
{question}
"""


    result = llm.call(prompt)

    if not result["success"]:
        raise Exception(result["error"])

    sql = result["content"].replace("```", "").strip()
    print("生成的 SQL：\n", sql,flush=True)

    if not validate_sql(sql):
        raise ValueError("生成SQL未通过安全校验")

    return sql, result["time"]