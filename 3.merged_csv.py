import pandas as pd

# Load both CSVs
berlin = pd.read_csv("berlin_cafes.csv")
munich = pd.read_csv("munich_cafes.csv")

# Add city column if missing
berlin["city"] = "Berlin"
munich["city"] = "Munich"

# Combine
cafes_all = pd.concat([berlin, munich], ignore_index=True)

# Drop duplicates by osm_id
cafes_all = cafes_all.drop_duplicates(subset="osm_id")

# Save merged dataset
cafes_all.to_csv("cafes_all.csv", index=False)

print(f"Unified dataset saved with {len(cafes_all)} cafés")
