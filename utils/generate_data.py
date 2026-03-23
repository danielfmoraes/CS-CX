import pandas as pd
import numpy as np
from faker import Faker

fake = Faker()

def generate_data(n=120):
    data = []

    for i in range(n):
        segment = np.random.choice(["SMB", "Mid", "Enterprise"], p=[0.5, 0.3, 0.2])
        
        revenue = {
            "SMB": np.random.randint(2000, 8000),
            "Mid": np.random.randint(8000, 25000),
            "Enterprise": np.random.randint(25000, 80000)
        }[segment]

        tickets = np.random.randint(5, 50)
        sla_breach = np.random.choice([0,1], p=[0.7,0.3])
        nps = np.random.randint(20, 90)
        churn_risk = np.random.choice([0,1], p=[0.8,0.2])
        expansion = np.random.choice([0,1], p=[0.6,0.4])

        data.append({
            "client": fake.company(),
            "segment": segment,
            "revenue": revenue,
            "tickets": tickets,
            "sla_breach": sla_breach,
            "nps": nps,
            "churn_risk": churn_risk,
            "expansion_opportunity": expansion
        })

    return pd.DataFrame(data)

if __name__ == "__main__":
    df = generate_data()
    df.to_csv("data/simulated_data.csv", index=False)