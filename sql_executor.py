#sql_executor
from db import engine
from sqlalchemy import text

def get_table_schema(table_name):
    query = f"DESCRIBE {table_name};"
    with engine.connect() as conn:
        result = conn.execute(text(query))
        columns = result.fetchall()

    schema_info = ""
    for col in columns:
        field = col[0]
        col_type = col[1]
        schema_info += f"{field} {col_type}\n"

    return schema_info


def execute_select_sql(sql):
    # 安全限制：只允许SELECT
    if not sql.strip().lower().startswith("select"):
        raise ValueError("只允许执行SELECT语句")

    with engine.connect() as conn:
        result = conn.execute(text(sql))
        rows = result.fetchall()
        columns = result.keys()

    return columns, rows