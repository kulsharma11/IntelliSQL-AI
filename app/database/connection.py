from sqlalchemy import create_engine
from dotenv import load_dotenv
import os

load_dotenv()


def get_engine(database_name):

    url = (
        f"mysql+pymysql://"
        f"{os.getenv('MYSQL_USER')}:"
        f"{os.getenv('MYSQL_PASSWORD')}@"
        f"{os.getenv('MYSQL_HOST')}:"
        f"{os.getenv('MYSQL_PORT')}/"
        f"{database_name}"
    )

    return create_engine(
        url,
        pool_pre_ping=True
    )