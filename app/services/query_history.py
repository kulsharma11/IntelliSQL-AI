import pandas as pd
from pathlib import Path

LOG_FILE = Path("logs/query_history.csv")


def save_query(question, sql):

    row = pd.DataFrame(
        [
            {
                "question": question,
                "sql": sql
            }
        ]
    )

    if LOG_FILE.exists():

        row.to_csv(
            LOG_FILE,
            mode="a",
            header=False,
            index=False
        )

    else:

        row.to_csv(
            LOG_FILE,
            index=False
        )