import pandas as pd
import numpy as np
from sklearn.preprocessing import OneHotEncoder
from sklearn.compose import ColumnTransformer

# Ustawienia wyświetlania DataFrame
pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)
pd.set_option('display.width', None)
pd.set_option('display.max_colwidth', None)

# Wczytanie danych
file_directory = r"../datasets/połączone_dekady_filtered3.csv"
df = pd.read_csv(file_directory)

# Usunięcie kolumny 'SquareFeetRange'


# Zmiana nazwy kolumny 'AveragePrice' na 'Price'
hot_encoder = OneHotEncoder()
hot_col = ['Neighborhood']

# Konfiguracja ColumnTransformer
preprocessing_pipeline = ColumnTransformer(
    transformers=[
        ('onehot', hot_encoder, hot_col),
    ]
)

# Transformacja danych i utworzenie nowego DataFrame
data_preprocessed = pd.DataFrame(
    preprocessing_pipeline.fit_transform(df),
    columns=list(preprocessing_pipeline.named_transformers_['onehot'].get_feature_names_out(hot_col)),
    index=df.index
)

df = df.drop(columns=hot_col).join(data_preprocessed)

def huber_loss(y_true, y_pred, delta=1.0):
  error = y_true - y_pred
  huber_loss = np.where(np.abs(error) < delta, 0.5 * error ** 2, delta * (np.abs(error) - 0.5 * delta))

  return np.mean(huber_loss)