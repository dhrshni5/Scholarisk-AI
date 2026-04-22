import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
import pickle

# Create dataset manually
data = {
    "sleep_hours": [4, 6, 7, 5, 3, 8, 6, 2, 7, 5, 4, 6, 7, 3, 8, 5, 6, 4, 7, 5],
    "study_hours": [2, 5, 6, 3, 1, 7, 5, 1, 6, 4, 2, 5, 6, 2, 7, 3, 5, 2, 6, 4],
    "screen_time": [8, 4, 3, 6, 9, 2, 5, 10, 3, 6, 8, 4, 3, 9, 2, 7, 5, 8, 3, 6],
    "stress_level": [9, 5, 4, 7, 10, 3, 6, 10, 4, 7, 9, 5, 4, 10, 3, 8, 6, 9, 4, 7],
    "breaks_per_day": [1, 3, 4, 2, 1, 5, 3, 1, 4, 2, 1, 3, 4, 1, 5, 2, 3, 1, 4, 2],
    "motivation_level": [2, 6, 7, 4, 1, 8, 6, 1, 7, 5, 2, 6, 7, 1, 8, 4, 6, 2, 7, 5],
    "burnout": [1, 0, 0, 1, 1, 0, 0, 1, 0, 1, 1, 0, 0, 1, 0, 1, 0, 1, 0, 1]
}

df = pd.DataFrame(data)

X = df.drop("burnout", axis=1)
y = df["burnout"]

# Train model
model = LogisticRegression()
model.fit(X, y)

# Save model
pickle.dump(model, open("model.pkl", "wb"))

print("Model trained and saved!")