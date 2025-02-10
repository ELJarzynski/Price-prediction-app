import pandas as pd

"""Settings of terminal setup"""
pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)
pd.set_option('display.width', None)
pd.set_option('display.max_colwidth', None)

file_directory = r"/housing_price_dataset.csv"
df = pd.read_csv(file_directory)

