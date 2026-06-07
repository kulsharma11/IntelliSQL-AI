import pandas as pd


def detect_chart_type(df):

    if len(df) == 0:
        return None

    numeric_cols = [
        col
        for col in df.columns
        if pd.api.types.is_numeric_dtype(df[col])
    ]

    categorical_cols = [
        col
        for col in df.columns
        if not pd.api.types.is_numeric_dtype(df[col])
    ]

    if len(numeric_cols) == 0:
        return None

    if len(categorical_cols) >= 1:

        x_col = categorical_cols[0]

        if any(
            keyword in x_col.lower()
            for keyword in ["date", "month", "year"]
        ):
            return {
                "type": "line",
                "x": x_col,
                "y": numeric_cols[-1]
            }

        return {
            "type": "bar",
            "x": x_col,
            "y": numeric_cols[-1]
        }

    return None