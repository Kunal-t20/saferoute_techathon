import joblib
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report

from preprocessing import preprocess_data


def train_model():

    # ----- LOAD & PREPROCESS -----
    X, y = preprocess_data(
        r"F:\Projects\techathon\backend\app\Data\AccidentsBig_cleaned.csv"
    )

    for col in X.columns:
        if str(X[col].dtype) == "string":
            X[col] = X[col].astype("object")

    # ----- COLUMN TYPES -----
    categorical_cols = X.select_dtypes(include=["object"]).columns
    numeric_cols = X.select_dtypes(exclude=["object"]).columns

    # ----- PREPROCESS PIPELINE -----
    preprocessor = ColumnTransformer(
        transformers=[
            ("cat", OneHotEncoder(handle_unknown="ignore"), categorical_cols),
            ("num", "passthrough", numeric_cols),
        ]
    )

    model = RandomForestClassifier(random_state=42)

    pipeline = Pipeline([
        ("preprocessor", preprocessor),
        ("model", model)
    ])

    # ----- HYPERPARAMETERS -----
    param_grid = {
        "model__n_estimators": [200, 300],
        "model__max_depth": [20, None],
        "model__min_samples_split": [2, 5]
    }

    # ----- TRAIN TEST SPLIT -----
    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=0.2,
        random_state=42,
        stratify=y
    )

    # ----- GRID SEARCH -----
    grid = GridSearchCV(
        pipeline,
        param_grid,
        cv=3,
        n_jobs=-1,
        verbose=1
    )

    grid.fit(X_train, y_train)

    best_model = grid.best_estimator_

    # ----- EVALUATION -----
    preds = best_model.predict(X_test)

    print("Accuracy:", accuracy_score(y_test, preds))
    print(classification_report(y_test, preds))
    print("Best Params:", grid.best_params_)

    # ----- SAVE MODEL -----
    joblib.dump(best_model, "risk_model.pkl")

    print("Model Saved!")


if __name__ == "__main__":
    train_model()
