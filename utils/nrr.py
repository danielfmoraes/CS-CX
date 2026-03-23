def calculate_nrr(df):
    base_revenue = df["revenue"].sum()

    churn_loss = df[df["churn_risk"] == 1]["revenue"].sum() * 0.3
    expansion_gain = df[df["expansion_opportunity"] == 1]["revenue"].sum() * 0.2

    final_revenue = base_revenue - churn_loss + expansion_gain

    nrr = (final_revenue / base_revenue) * 100

    return round(nrr, 2)