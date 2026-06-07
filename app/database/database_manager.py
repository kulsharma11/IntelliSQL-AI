from sqlalchemy import text

from app.database.connection import get_engine


def get_databases():

    engine = get_engine("mysql")

    with engine.connect() as conn:

        result = conn.execute(
            text("SHOW DATABASES")
        )

        dbs = [
            row[0]
            for row in result
        ]

    return dbs