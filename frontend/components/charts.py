import plotly.express as px


def create_chart(df, chart_info):

    chart_type = chart_info["type"]
    x_col = chart_info["x"]
    y_col = chart_info["y"]

    if chart_type == "bar":

        return px.bar(
            df,
            x=x_col,
            y=y_col,
            title=f"{y_col} by {x_col}"
        )

    if chart_type == "line":

        return px.line(
            df,
            x=x_col,
            y=y_col,
            markers=True,
            title=f"{y_col} by {x_col}"
        )

    return None