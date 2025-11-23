# ml.py
import numpy as np
import pandas as pd
from sklearn.linear_model import LogisticRegression
from joblib import dump, load
import os

MODEL_PATH = "model_joblib.pkl"

def _features_from_df(df):
    """
    Given DataFrame with columns: income, credit_score, employment_years, debt_to_income, amount
    returns X (np.array) and y (if present)
    """
    X = df[['income', 'credit_score', 'employment_years', 'debt_to_income', 'amount']].values
    y = None
    if 'label' in df.columns:
        y = df['label'].values
    return X, y

def train_from_dataframe(df):
    """Train logistic regression on provided DataFrame with label column (1 = approve, 0 = reject)."""
    X, y = _features_from_df(df)
    if y is None:
        raise ValueError("DataFrame must contain 'label' column")
    model = LogisticRegression(max_iter=1000)
    model.fit(X, y)
    dump(model, MODEL_PATH)
    return model

def ensure_model_exists():
    """If model file doesn't exist, create a default baseline model trained on tiny synthetic data."""
    if not os.path.exists(MODEL_PATH):
        df = pd.DataFrame([
            # income, credit_score, employment_years, debt_to_income, amount, label
            [70000, 750, 5, 0.25, 50000, 1],
            [30000, 600, 1, 0.50, 15000, 0],
            [50000, 680, 3, 0.30, 25000, 1],
            [25000, 580, 1, 0.60, 10000, 0],
            [120000, 800, 10, 0.10, 150000, 1],
            [40000, 640, 2, 0.40, 20000, 0],
            # NEW DATA: Low credit score approvals
            [45000, 350, 2, 0.30, 20000, 1],
            [35000, 320, 3, 0.25, 10000, 1],
            [55000, 400, 4, 0.35, 30000, 1],
            # NEW DATA: Modest score approvals (around 300)
            [40000, 302, 2, 0.28, 12000, 1],
            [38000, 305, 3, 0.30, 15000, 1],
            [30000, 300, 1, 0.20, 5000, 1]
        ], columns=['income','credit_score','employment_years','debt_to_income','amount','label'])
        train_from_dataframe(df)

def load_model():
    ensure_model_exists()
    return load(MODEL_PATH)

def predict_single(model, feature_dict):
    """
    feature_dict: keys income, credit_score, employment_years, debt_to_income, amount
    returns: decision ("APPROVE"/"REJECT"), confidence (prob of predicted class), raw_probs, contributions (coef * x)
    """
    X = [[feature_dict['income'],
          feature_dict['credit_score'],
          feature_dict['employment_years'],
          feature_dict['debt_to_income'],
          feature_dict['amount']]]
    probs = model.predict_proba(X)[0]  # [prob_class0, prob_class1] assuming label mapping (0 reject,1 approve)
    pred = model.predict(X)[0]
    conf = max(probs)
    # compute simple linear contributions using model.coef_
    coefs = model.coef_[0]  # shape (n_features,)
    contributions = (coefs * np.array(X[0])).tolist()
    feature_names = ['income','credit_score','employment_years','debt_to_income','amount']
    contrib_map = dict(zip(feature_names, contributions))
    return ("APPROVE" if pred==1 else "REJECT"), float(conf), probs.tolist(), contrib_map
