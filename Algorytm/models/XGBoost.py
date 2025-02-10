from datasets.data_to_use import *
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error, r2_score
import matplotlib.pyplot as plt
import xgboost as xgb

X_train, X_test, y_train, y_test = train_test_split(df.drop(columns=['Price']), df['Price'],
                                                    test_size=0.33, random_state=42)
X_train, X_val, y_train, y_val = train_test_split(X_train, y_train, test_size=0.33, random_state=42)

model = xgb.XGBRegressor(
    n_estimators=200,
    learning_rate=0.1,
    max_depth=1,
    min_split_loss=0,
    min_child_weight=1,
    subsample=0.8,
    colsample_bytree=0.8,
    objective='reg:squarederror',
    n_jobs=-1,
    random_state=42
)
model.fit(X_train, y_train)

y_predict_full = model.predict(df.drop(columns=['Price']))
y_predict_val = model.predict(X_val)
y_predict_test = model.predict(X_test)

huber_loss_val = mean_absolute_error(y_val, y_predict_val)
huber_loss_test = mean_absolute_error(y_test, y_predict_test)
r2 = r2_score(y_test, y_predict_test)

print("Huber Loss na zbiorze walidacyjnym:", huber_loss_val)
print("Huber Loss na zbiorze testowym:", huber_loss_test)
print(r2)
plt.figure(figsize=(10, 6))
plt.scatter(df.index, df['Price'], color="blue", label="True values", alpha=0.6, s=10)
plt.scatter(df.index, y_predict_full, color="red", label="Predicted values", alpha=0.6, s=10)
plt.title(f'Regressor: {type(model).__name__}')
plt.xlabel("Index")
plt.ylabel("Price")
plt.legend()
plt.text(0.5, -0.1, f"huber_loss_val = {huber_loss_val:.4f}\nhuber_loss_test = {huber_loss_test:.4f}",
         ha="center", va="top", transform=plt.gca().transAxes, fontsize=10, color="black")
plt.savefig("../model_plots/October_30_XGBoost.png", bbox_inches="tight")

# Wyświetlenie wykresu
plt.show()
