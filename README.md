# Ethical AI Banking System

A Flask-based banking application that uses Explainable AI (XAI) to make fair and transparent loan decisions. This project demonstrates how AI can be used in finance while maintaining ethical standards and providing clear explanations for decisions.

## 🚀 Features

*   **AI-Powered Loan Decisions**: Uses a Machine Learning model to assess loan applications based on income, credit score, and other factors.
*   **Transparent Explanations**: If a loan is rejected, the system provides clear, human-readable reasons (e.g., "Debt-to-Income ratio too high").
*   **Ethical & Fair**: Designed to avoid bias and ensure fairness in lending.
*   **User Dashboard**: View loan history, credit score insights, and spending analysis.
*   **Localized for India**: All currency is displayed in **Rupees (₹)**.
*   **Inclusive Criteria**: Accepts credit scores as low as **300** to help underserved customers.

## 🛠️ Setup & Installation

1.  **Prerequisites**: Ensure you have Python installed.
2.  **Install Dependencies**:
    ```bash
    pip install -r requirements.txt
    ```
3.  **Initialize Database**:
    The application automatically initializes the database (`instance/app.sqlite`) on the first run.

## ▶️ Running the Application

Run the following command in your terminal:

```bash
python app.py
```

Open your browser and go to: `http://127.0.0.1:5000`

## 🔑 Login Credentials

You can sign up as a new user, or use the default admin account:

*   **Email**: `admin@trustbank.com`
*   **Password**: `admin123`

## 📝 Loan Approval Criteria

The system uses a hybrid approach of **Machine Learning** + **Safety Rules**:

*   **Minimum Credit Score**: 300
*   **Minimum Income**: ₹25,000/year
*   **Debt-to-Income Ratio**: Should be below 43%
*   **Employment**: At least 1 year preferred

*Note: The system is designed to be modest and will approve loans for scores between 300-600 if other financial health indicators are positive.*

## 📂 Project Structure

*   `app.py`: Main application logic and routes.
*   `models.py`: Database models (User, LoanApplication).
*   `ml.py`: Machine Learning model training and prediction logic.
*   `templates/`: HTML files for the user interface.
*   `instance/`: Contains the SQLite database.

## 🔄 Recent Updates

*   **Currency Update**: Changed all symbols from Dollar ($) to Rupee (₹).
*   **Policy Update**: Lowered minimum credit score requirement from 600 to 300.
*   **Bug Fix**: Resolved database schema issues and improved Windows compatibility.