import os
import time
import pandas as pd
import json
import requests

# Get absolute path of the file
file_name = "report.xlsx"
file_path = os.path.join(os.getcwd(), file_name)

# Check if file exists
if not os.path.exists(file_path):
    raise FileNotFoundError(f"File not found: {file_path}")

# Load the Excel file
xls = pd.ExcelFile(file_path)

# Load the relevant sheet
sheet_name = "Consultadd Engineering Hiring F"
df = pd.read_excel(xls, sheet_name=sheet_name)

# Preserve all original columns
original_columns = df.copy()


df.columns.values[1] = "Student Name"
df.columns.values[2] = "Email"
df.columns.values[3] = "Test Start Time"
df.columns.values[4] = "Answer 1"
df.columns.values[5] = "Answer 2"

# Extract questions (first row of columns 5 and 6, which are indexed at 4 and 5)
questions = [df.iloc[4, 4], df.iloc[4, 5]]

# Extract student answers (starting from row 5 onwards, columns 5 and 6)
df = df.iloc[5:].reset_index(drop=True)

# Replace missing answers with "Empty"
df.iloc[:, 4] = df.iloc[:, 4].fillna("Empty")
df.iloc[:, 5] = df.iloc[:, 5].fillna("Empty")

# Define API endpoint
API_ENDPOINT = os.getenv("API_ENDPOINT")

# Store responses
scores1, explanations1, scores2, explanations2 = [], [], [], []

# Process each row one by one
for i in range(len(df)):
    answer1 = df.iloc[i, 4]
    answer2 = df.iloc[i, 5]

    payload = {
        "questions": [
            {"description": questions[0]},
            {"description": questions[1]}
        ],
        "solutions": [[answer1], [answer2]]
    }

    headers = {"Content-Type": "application/json"}

    while True:
        response = requests.post(API_ENDPOINT, data=json.dumps(payload), headers=headers)
        if response.status_code == 200:
            result = response.json()
            break
        else:
            print(f"Error: {response.status_code}")

            # print(f"Error: {response.status_code}, Retrying in 10 seconds...")
            # time.sleep(10)

    # Extract scores and explanations
    evaluation_json1 = json.loads(result["results"][0]["evaluation"].strip("```json\n"))
    evaluation_json2 = json.loads(result["results"][1]["evaluation"].strip("```json\n"))
    
    scores1.append(evaluation_json1["Score"])
    explanations1.append("\n".join(evaluation_json1["Explanation"]))
    scores2.append(evaluation_json2["Score"])
    explanations2.append("\n".join(evaluation_json2["Explanation"]))

    print(f"Processed row {i+1}")

   

# Ensure lists match df length
while len(scores1) < len(df):
    scores1.append(0)
    explanations1.append("No response from API")
while len(scores2) < len(df):
    scores2.append(0)
    explanations2.append("No response from API")

# Add new columns to original dataframe
df["Score1"], df["Explanation1"] = scores1, explanations1
df["Score2"], df["Explanation2"] = scores2, explanations2

# Merge back with original columns
final_df = original_columns.iloc[5:].reset_index(drop=True)
final_df["Score1"], final_df["Explanation1"] = scores1, explanations1
final_df["Score2"], final_df["Explanation2"] = scores2, explanations2

# Save updated results to CSV file
updated_file_path = os.path.join(os.getcwd(), "updated_results.csv")
final_df.to_csv(updated_file_path, index=False)

print(f"Updated file saved at: {updated_file_path}")
