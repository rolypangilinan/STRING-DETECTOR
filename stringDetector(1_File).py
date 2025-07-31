#%%
# WORKING
# CHECK CSV FILE AND NEED TO CHANGE PATH LOCATION




# MariaDB connection
# OPEN FC1DataBase.csv, REMOVED DOUBLE QUOTE AT "MODEL_CODE"
# Error: An error occured: can only concatenate str(not "float) to str


# import mysql.connector as mariadb
import pandas as pd

# mariadb_connection = mariadb.connect(user='hpi.python', password='hpi.python', database='fc_1_data_db', host='192.168.2.148', port=3306)
# create_cursor = mariadb_connection.cursor()

# sqlStatement = f"SELECT * FROM database_data"
# create_cursor.execute(sqlStatement)
# myresult = create_cursor.fetchall()

# # Get column names from cursor description
# columns = [desc[0] for desc in create_cursor.description]

# # Create DataFrame
# df = pd.DataFrame(myresult, columns=columns)

# Convert DataFrame to CSV
# df.to_csv('output.csv', index=False)







# SAVED TO "cleanCorrelation" AS DATAFRAME

# File locations
# input_file = r"\\192.168.2.19\ai_team\AI Program\Outputs\CompiledProcess\FC1DataBase.csv"
# input_file = r"\\192.168.2.19\ai_team\INDIVIDUAL FOLDER\June-San\database_data_202507290944.csv"    #whole
input_file = r"\\192.168.2.19\ai_team\INDIVIDUAL FOLDER\June-San\DataBase 073025.csv"   #filtered

# Load the CSV file
try:
    df = pd.read_csv(input_file, encoding="latin1")
except UnicodeDecodeError:
    df = pd.read_csv(input_file, encoding="ISO-8859-1", errors="replace")

# Remove double quotes in "MODEL_CODE" column if it exists
if "MODEL_CODE" in df.columns:
    df["MODEL_CODE"] = df["MODEL_CODE"].astype(str).str.replace('"', '', regex=False)   
    #(.astype(str): Ensures all values in the "MODEL_CODE" column are treated as strings.) 
    # (.str.replace('"', '', regex=False): Removes all double quotes (") from those string values. 
    # The regex=False tells Pandas to treat the double quote as a literal character, not a regex pattern.)
else:
    print("Error: 'MODEL_CODE' column not found!")

# Store the cleaned DataFrame in memory
cleanCorrelation = df.copy()

print("Double quote removed and saved to (cleanCorrelation)")
# print(f"Double quote removed and saved to {cleanCorrelation}")

# Filter unwanted model codes
df = df[~df["MODEL_CODE"].isin(["60CAT0203M"])]

print(f'REMOVED "60CAT0203M" AND SAVED TO {df}')









# REMOVE UNWANTED VALUES
import pandas as pd

# List of values to remove
values_to_remove = [
    # "NG PRESSURE", "NG AT PROCESS1", "NG AT PROCESS2", "NG AT PROCESS3", "NG AT PROCESS4", "NG AT PROCESS5",
    # "REPAIRED AT PROCESS4", "REPAIRED AT PROCESS3", "RE PI", "MASTER PUMP",
    # "NG PRESSURE AT PROCESS5", "No Data Found", "INSPECTION ONLY", "REPAIRED AT PROCESS2"
]

# Ensure all columns are treated as strings before filtering
cleanCorrelation = cleanCorrelation.astype(str)

# Remove rows where any column contains unwanted values
cleanCorrelation2 = cleanCorrelation[~cleanCorrelation.apply(lambda row: row.isin(values_to_remove).any(), axis=1)] 
#(row.isin(values_to_remove) For each row in cleanCorrelation, it checks whether any cell in that row matches a value from the list values_to_remove.) 
#(.any() If any value in that row matches, this returns True.)
#(.apply(..., axis=1) Runs this logic row by row (because axis=1 means apply across columns).)
#(~ (bitwise NOT) This negates the result — so True becomes False, and vice versa. Meaning: only keep rows that do not contain any of the values_to_remove.)
#(Indexing The result is used to filter cleanCorrelation, assigning the cleaned DataFrame to cleanCorrelation2.) (LAMBDA It means: “For each row in the DataFrame, check if any of its values are in the values_to_remove list.”)

# Display confirmation message
print("Removed unwanted values done, saved to (cleanCorrelation2)")







import pandas as pd

# Define exemption column(s)
exempt_columns = [
    "TIME", "MODEL_CODE", "Process_1_NAME"
                  
]  # Replace with your actual column name(s)

# Create dictionary to hold results
string_counts = {}

for col in cleanCorrelation2.columns:
    if col not in exempt_columns:
        count = cleanCorrelation2[col].apply(lambda x: isinstance(x, str) and any(char.isalpha() for char in x)).sum()
        string_counts[col] = count

# Convert results to DataFrame
string_counts_df = pd.DataFrame(list(string_counts.items()), columns=["Column Name", "String Count"])

# Save to CSV
string_counts_df.to_csv("string_counts_summary.csv", index=False)

print(" String counts saved to 'string_counts_summary.csv'")

# # Remove rows where any column contains the string "INSPECTION ONLY"
# cleanCorrelation2 = cleanCorrelation2[~cleanCorrelation2.apply(lambda row: row.astype(str).str.contains("INSPECTION ONLY", case=False, na=False).any(), axis=1)]

# print(" Rows containing 'INSPECTION ONLY' have been removed.")

# Save the cleaned DataFrame to CSV
cleanCorrelation2.to_csv("cleanCorrelation2_output.csv", index=False)

print(" 'cleanCorrelation2' DataFrame saved to 'cleanCorrelation2_output.csv'")




#%%















# import pandas as pd

# # 📁 File paths
# input_path = r"\\192.168.2.19\ai_team\AI Program\Outputs\CompiledProcess\FC1DataBase.csv"
# output_summary_path = r"\\192.168.2.19\ai_team\INDIVIDUAL FOLDER\June-San\p2LTG\p2LTG_TransferData\MatchSummary.csv"
# output_clean_path = r"\\192.168.2.19\ai_team\INDIVIDUAL FOLDER\June-San\p2LTG\p2LTG_TransferData\cleanCorrelation2.csv"

# # 📥 Load CSV with encoding fallback
# try:
#     df = pd.read_csv(input_path, encoding="latin-1")
# except UnicodeDecodeError:
#     df = pd.read_csv(input_path, encoding="ISO-8859-1", errors="replace")

# # 🔍 Define parameters
# columns_to_ignore = ['MODEL_CODE']
# search_string = 'apple'

# # ✅ Filter columns to process
# columns_to_count = [col for col in df.columns if col not in columns_to_ignore]

# # 🔢 Count non-empty cells
# non_empty_count = df[columns_to_count].astype(str).applymap(lambda x: bool(x.strip())).sum().sum()
# print(f"\n📊 Total non-empty cells across allowed columns (excluding {columns_to_ignore}): {non_empty_count}")

# # 🔎 Search for matches and collect results
# print(f"\n🔍 Searching for string '{search_string}' across columns...\n")
# match_summary = []

# for col in columns_to_count:
#     match_count = df[col].astype(str).str.contains(search_string, case=False, na=False).sum()
#     if match_count:
#         print(f"✅ {match_count} match(es) found in column: {col}")
#         match_summary.append({'Column': col, 'Match Count': match_count})

# # 🧮 Display total matches
# total_matches = sum(item['Match Count'] for item in match_summary)
# print(f"\n📈 Total number of string matches across all columns: {total_matches}")

# # 💾 Save match summary
# match_df = pd.DataFrame(match_summary)
# match_df.to_csv(output_summary_path, index=False)
# print(f"\n✅ Match summary saved to:\n{output_summary_path}")

# # 💾 Save cleanCorrelation2 DataFrame
# cleanCorrelation2.to_csv(output_clean_path, index=False)
# print(f"\n✅ cleanCorrelation2 DataFrame saved to:\n{output_clean_path}")


# %%
