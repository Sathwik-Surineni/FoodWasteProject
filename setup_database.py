import pandas as pd
from sqlalchemy import create_engine

# Load datasets
providers = pd.read_csv("providers_data.csv")
receivers = pd.read_csv("receivers_data.csv")
food = pd.read_csv("food_listings_data.csv")
claims = pd.read_csv("claims_data.csv")

# Create SQLite database
engine = create_engine("sqlite:///food_waste.db")

# Save into SQL tables
providers.to_sql("providers", engine, if_exists="replace", index=False)
receivers.to_sql("receivers", engine, if_exists="replace", index=False)
food.to_sql("food_listings", engine, if_exists="replace", index=False)
claims.to_sql("claims", engine, if_exists="replace", index=False)

print("✅ Database setup complete: food_waste.db created.")
