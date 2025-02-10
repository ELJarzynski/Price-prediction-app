from datasets.data_to_use import *
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
import matplotlib.pyplot as plt
import os

# Upewnienie się, że folder model_plots istnieje
os.makedirs("./model_plots", exist_ok=True)

# Podział danych na zbiory treningowy, walidacyjny i testowy
X_train, X_test, y_train, y_test = train_test_split(df.drop(columns=['Price']), df['Price'],
                                                    test_size=0.33, random_state=42)
X_train, X_val, y_train, y_val = train_test_split(X_train, y_train, test_size=0.33, random_state=42)

# Trenowanie modelu regresji liniowej
lm = LinearRegression(n_jobs=-1, fit_intercept=True)
lm.fit(X_train, y_train)

# Predykcje na pełnym zbiorze danych
y_predict_full = lm.predict(df.drop(columns=['Price']))

# Obliczenie wartości Huber Loss dla walidacji i testu
y_predict_val = lm.predict(X_val)
y_predict_test = lm.predict(X_test)
huber_loss_val = huber_loss(y_val, y_predict_val)
huber_loss_test = huber_loss(y_test, y_predict_test)

# Wydruk wartości Huber Loss
print("Huber Loss na zbiorze walidacyjnym:", huber_loss_val)
print("Huber Loss na zbiorze testowym:", huber_loss_test)

# Tworzenie wykresu scatter dla pełnego zestawu danych
plt.figure(figsize=(10, 6))
plt.scatter(df.index, df['Price'], color="blue", label="True values", alpha=0.6, s=10)
plt.scatter(df.index, y_predict_full, color="red", label="Predicted values", alpha=0.6, s=10)

# Ustawienia wykresu
plt.title(f'Regressor: {type(lm).__name__}')
plt.xlabel("Index")
plt.ylabel("Price")
plt.legend()

# Dodanie wartości Huber Loss bezpośrednio na wykresie
plt.text(0.5, -0.1, f"huber_loss_val = {huber_loss_val:.4f}\nhuber_loss_test = {huber_loss_test:.4f}",
         ha="center", va="top", transform=plt.gca().transAxes, fontsize=10, color="black")

# Zapis wykresu do folderu model_plots jako October_30_model.png
plt.savefig("../model_plots/October_30_LinearRegressor.png", bbox_inches="tight")

# Wyświetlenie wykresu
plt.show()
