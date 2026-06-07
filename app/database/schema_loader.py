from sqlalchemy import inspect

from app.database.connection import get_engine


def get_schema(database_name):

    engine = get_engine(database_name)
    inspector = inspect(engine)

    schema_text = ""

    tables = inspector.get_table_names()

    for table in tables:

        schema_text += f"\n{table}(\n"

        columns = inspector.get_columns(table)

        for column in columns:
            schema_text += f"    {column['name']},\n"

        schema_text += ")\n"

    return schema_text