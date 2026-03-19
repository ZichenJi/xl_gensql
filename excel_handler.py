import pandas as pd
from db import engine
from llm_table_namer import generate_table_name_by_llm


def excel_to_mysql(file_path, original_filename):
    df = pd.read_excel(file_path)

    table_name = generate_table_name_by_llm(original_filename)

    df.to_sql(table_name, engine, if_exists="replace", index=False)

    return table_name