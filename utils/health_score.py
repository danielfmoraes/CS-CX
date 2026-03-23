def calculate_health_score(df):
    score = (
        (df["nps"] * 0.3) +
        ((1 - df["sla_breach"]) * 30) +
        ((1 - df["churn_risk"]) * 40) +
        (df["expansion_opportunity"] * 20)
    )
    
    df["health_score"] = score

    def label(score):
        if score >= 70:
            return "Healthy"
        elif score >= 40:
            return "Warning"
        else:
            return "Critical"

    df["health_label"] = df["health_score"].apply(label)
    return df