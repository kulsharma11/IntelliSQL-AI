import pandas as pd

from app.database.connection import get_engine


def execute_query(sql: str, database_name: str):

    engine = get_engine(database_name)

    df = pd.read_sql(
        sql,
        engine
    )

    return df