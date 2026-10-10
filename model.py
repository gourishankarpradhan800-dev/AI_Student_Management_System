import numpy as np
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score

FEATURES = [
    "attendance",
    "study_hours",
    "previous_marks"
]

TARGET = "final_marks"


def train_model(data):
    if len(data) < 5:
        raise ValueError(
            "At least 5 student records are required for a demonstration."
        )

    X = data[FEATURES]
    y = data[TARGET]

    if y.nunique() < 2:
        raise ValueError(
            "The target must contain at least two different marks."
        )

    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=0.25,
        random_state=42
    )

    model = RandomForestRegressor(
        n_estimators=100,
        max_depth=5,
        random_state=42
    )

    model.fit(X_train, y_train)

    predictions = model.predict(X_test)

    mae = mean_absolute_error(y_test, predictions)
    rmse = np.sqrt(mean_squared_error(y_test, predictions))

    if len(y_test) >= 2:
        r2 = r2_score(y_test, predictions)
    else:
        r2 = None

    metrics = {
        "MAE": float(mae),
        "RMSE": float(rmse),
        "R2": float(r2) if r2 is not None else None
    }

    return model, metrics


def predict_marks(model, attendance, study_hours, previous_marks):
    input_data = [[attendance, study_hours, previous_marks]]

    prediction = model.predict(input_data)[0]

    return float(np.clip(prediction, 0, 100))


def generate_recommendations(attendance, study_hours, previous_marks):
    recommendations = []

    if attendance < 75:
        recommendations.append(
            "Improve attendance and attend classes regularly."
        )

    if study_hours < 2:
        recommendations.append(
            "Consider establishing a consistent daily study routine."
        )

    if previous_marks < 40:
        recommendations.append(
            "Review foundational concepts and seek help from a teacher."
        )
    elif previous_marks < 60:
        recommendations.append(
            "Practice more questions and revise difficult topics."
        )

    if not recommendations:
        recommendations.append(
            "Maintain your current study habits and revise regularly."
        )

    return recommendations