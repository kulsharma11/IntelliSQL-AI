from app.chains.insight_chain import insight_chain


def generate_insights(question, df):

    sample_data = df.to_string(index=False)

    insights = insight_chain.invoke(
        {
            "question": question,
            "data": sample_data
        }
    )

    return insights