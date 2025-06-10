# Part 3: The Stowaway Protocol - Analysis and Prototype Implementation

import pandas as pd

# Load data from CSV file (update the path as needed)
file_path = "/Users/A/Downloads/Dataset for Group Project-20250605/Compartment_Sensor_Data.csv"
df = pd.read_csv(file_path)

df.rename(columns={
    "Compartment ID": "Compartment_ID",
    "Crew Movement Count": "Crew_Movement",
    "Oxygen Anomaly (%)": "Oxygen_Anomaly",
    "Heat Deviation (°C)": "Heat_Deviation"
}, inplace=True)


# Step 1: Preprocessing
# Convert negative heat deviation to 0 (we only consider positive heat anomalies)
df["Heat_Component"] = df["Heat_Deviation"].apply(lambda x: max(0, x))

# Step 2: Likelihood Scoring Formula
# Score = 0.5 * Oxygen Anomaly + 0.3 * Heat Component + 0.2 * Crew Movement
df["Score"] = (
    0.5 * df["Oxygen_Anomaly"] +
    0.3 * df["Heat_Component"] +
    0.2 * df["Crew_Movement"]
)

# Step 3: Ranking Compartments by Score (Descending)
df_sorted = df.sort_values(by="Score", ascending=False).reset_index(drop=True)

# Step 4: Calculate Probability Distribution based on Scores
total_score = df_sorted["Score"].sum()
df_sorted["Probability"] = df_sorted["Score"] / total_score

# Step 5: Calculate Expected Number of Searches
# Expected Value = sum(i * p_i) for i from 1 to n
df_sorted["Search_Position"] = df_sorted.index + 1
df_sorted["Expected_Value_Component"] = df_sorted["Search_Position"] * df_sorted["Probability"]
expected_searches = df_sorted["Expected_Value_Component"].sum()

# Output Results
print("Top 10 Compartments to Search:")
print(df_sorted[["Compartment_ID", "Score", "Probability", "Search_Position"]].head(10))
print(f"\nExpected Number of Searches to Find the Stowaway: {expected_searches:.2f}")