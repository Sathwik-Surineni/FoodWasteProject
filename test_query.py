import pandas as pd
from sqlalchemy import create_engine

engine = create_engine("sqlite:///food_waste.db")

query = "SELECT city, COUNT(*) as provider_count FROM providers GROUP BY city"
df = pd.read_sql(query, engine)

print(df)
