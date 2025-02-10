import pandas as pd

# Paths to CSV files
file_1 = "../datasets/decades/dekada2010-2019.csv"
file_2 = "../datasets/decades/dekada2000-2009.csv"
file_3 = "../datasets/decades/dekada1950-1959.csv"
file_4 = "../datasets/decades/dekada1960-1969.csv"
file_5 = "../datasets/decades/dekada1970-1979.csv"
file_6 = "../datasets/decades/dekada1980-1989.csv"
file_7 = "../datasets/decades/dekada1990-1999.csv"

# Load files into DataFrames
df1 = pd.read_csv(file_1)
df2 = pd.read_csv(file_2)
df3 = pd.read_csv(file_3)
df4 = pd.read_csv(file_4)
df5 = pd.read_csv(file_5)
df6 = pd.read_csv(file_6)
df7 = pd.read_csv(file_7)

# Combine DataFrames
combined_df = pd.concat([df1, df2, df3, df4, df5, df6, df7], ignore_index=True)

# Rename and drop unnecessary columns
df = combined_df.rename(columns={'AveragePrice': 'Price'})
df = df.drop(columns=['SquareFeetRange'], errors='ignore')

# Ensure 'Price' is in numeric format and handle errors
df['Price'] = pd.to_numeric(df['Price'], errors='coerce')

# Remove rows with NaN values in 'Price'
df = df.dropna(subset=['Price'])

# Remove rows where price is less than 100,000
df_filtered = df[df['Price'] >= 100000]

# Function to remove anomalies based on percentiles
def remove_anomalies(group):
    lower_bound = group['Price'].quantile(0.10)  # 10th percentile
    upper_bound = group['Price'].quantile(0.90)  # 90th percentile
    return group[(group['Price'] >= lower_bound) & (group['Price'] <= upper_bound)]

# Apply the anomaly removal function to each group based on 'AverageSquareFeet'
df_cleaned = df_filtered.groupby('AverageSquareFeet').apply(remove_anomalies).reset_index(drop=True)

# Save the cleaned DataFrame to a new CSV file
df_cleaned.to_csv("połączone_dekady_filtered3.csv", index=False)

print("Zapisano przefiltrowany plik CSV jako 'połączone_dekady_filtered2.csv'.")
