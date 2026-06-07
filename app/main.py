from app.chains.sql_chain import sql_chain
from app.database.schema_loader import get_schema
from app.services.sql_validator import validate_sql
from app.database.query_executor import execute_query
from app.services.query_history import save_query

def main():

    print("=" * 50)
    print("Natural Language SQL Analytics")
    print("=" * 50)

    question = input("\nAsk a question: ")

    schema = get_schema()

    print("\nGenerating SQL...\n")

    sql = sql_chain.invoke(
        {
            "question": question,
            "schema": schema
        }
    )

    save_query(question, sql)
    print("Generated SQL:\n")
    print(sql)

    if sql.strip() == "SCHEMA_ERROR":
        print("\n❌ Cannot answer using current database schema.")
        return

    valid, message = validate_sql(sql)

    if not valid:
        print(f"\n❌ Validation Failed: {message}")
        return

    print("\n✅ SQL Valid")

    try:

        df = execute_query(sql)

        print("\nResults:\n")

        if df.empty:
            print("No records found")

        else:
            print(df)

    except Exception as e:

        print(f"\n❌ Query Execution Error:\n{e}")


if __name__ == "__main__":
    main()