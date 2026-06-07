import sqlglot

FORBIDDEN = {
    "DELETE",
    "UPDATE",
    "INSERT",
    "DROP",
    "ALTER",
    "TRUNCATE",
    "CREATE"
}

def validate_sql(sql: str):

    try:
        parsed = sqlglot.parse_one(sql)

    except Exception:
        return False, "Invalid SQL"

    sql_upper = sql.upper()

    for keyword in FORBIDDEN:

        if keyword in sql_upper:
            return False, f"{keyword} not allowed"

    if not sql_upper.strip().startswith("SELECT"):
        return False, "Only SELECT queries allowed"

    return True, "Valid"