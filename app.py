from flask import Flask, render_template, request, redirect, url_for, session, flash
from datetime import datetime
import os
import sys

# Add current directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from models import db, User, LoanApplication, init_db

# Try to import ML module, but don't fail if it's not available
try:
    from ml import load_model, predict_single
    ML_AVAILABLE = True
except ImportError as e:
    print(f"Warning: ML module not available: {e}")
    ML_AVAILABLE = False
    def load_model():
        return None
    def predict_single(model, features):
        # Fallback decision logic
        if features.get('credit_score', 0) >= 650 and features.get('debt_to_income', 1) < 0.4:
            return 'APPROVE', 0.75, [0.25, 0.75], {}
        return 'REJECT', 0.65, [0.65, 0.35], {}

app = Flask(__name__)
app.secret_key = 'your-secret-key-change-in-production'

# Database configuration
basedir = os.path.abspath(os.path.dirname(__file__))
db_path = os.path.join(basedir, "instance")
os.makedirs(db_path, exist_ok=True)
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{os.path.join(db_path, "app.sqlite")}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

# Initialize database on startup
try:
    with app.app_context():
        init_db(app)
        print("[OK] Database initialized successfully")
except Exception as e:
    print(f"[WARNING] Database initialization warning: {e}")

# Helper filters
@app.template_filter('initials')
def initials_filter(name):
    if not name:
        return 'U'
    parts = name.strip().split()
    if len(parts) >= 2:
        return (parts[0][0] + parts[-1][0]).upper()
    return name[:2].upper() if len(name) >= 2 else name[0].upper()

@app.template_filter('currency')
def currency_filter(value):
    try:
        return f"₹{float(value):,.0f}"
    except (ValueError, TypeError):
        return value

# ---------------- LOGIN ---------------- 
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email', '').strip()
        password = request.form.get('password', '').strip()

        if not email or not password:
            flash('Email and password are required!', 'danger')
            return render_template('login.html', email=email)

        try:
            user = User.query.filter_by(email=email).first()
            if user:
                if user.check_password(password):
                    session['user_id'] = user.id
                    session['user'] = {
                        'id': user.id,
                        'name': user.name,
                        'email': user.email,
                        'type': 'admin' if user.is_admin else 'customer'
                    }
                    flash(f'Welcome {user.name}!', 'success')
                    return redirect(url_for('dashboard'))
                else:
                    flash('Incorrect password!', 'danger')
                    return render_template('login.html', email=email)
            else:
                flash('No account found. Please sign up.', 'info')
                return redirect(url_for('signup', email=email))
        except Exception as e:
            flash(f'An error occurred: {str(e)}', 'danger')
            print(f"Login error: {e}")
            return render_template('login.html', email=email)
    
    return render_template('login.html')

# ---------------- SIGNUP ---------------- 
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    prefill_email = request.args.get('email', '')
    if request.method == 'POST':
        name = request.form.get('name', '').strip()
        email = request.form.get('email', '').strip().lower()
        password = request.form.get('password', '').strip()

        # Validation
        if not name or not email or not password:
            flash('All fields are required!', 'danger')
            return render_template('signup.html', email=email)
        
        if len(password) < 6:
            flash('Password must be at least 6 characters long!', 'danger')
            return render_template('signup.html', email=email, name=name)
        
        if '@' not in email or '.' not in email:
            flash('Please enter a valid email address!', 'danger')
            return render_template('signup.html', email=email, name=name)

        try:
            # Check if user already exists
            existing_user = User.query.filter_by(email=email).first()
            if existing_user:
                flash('Email already registered! Please login instead.', 'danger')
                return redirect(url_for('login', email=email))

            # Create new user
            user = User(name=name, email=email, is_admin=False)
            user.set_password(password)
            db.session.add(user)
            db.session.commit()

            # Automatically log in the new user
            session['user_id'] = user.id
            session['user'] = {
                'id': user.id,
                'name': user.name,
                'email': user.email,
                'type': 'customer'
            }
            flash(f'Account created successfully! Welcome {user.name}!', 'success')
            return redirect(url_for('dashboard'))
            
        except Exception as e:
            db.session.rollback()
            flash(f'Error creating account: {str(e)}', 'danger')
            print(f"Signup error: {e}")
            return render_template('signup.html', email=email, name=name)

    return render_template('signup.html', email=prefill_email)

# ---------------- DASHBOARD ---------------- 
@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    user = User.query.get(session['user_id'])
    if not user:
        session.pop('user_id', None)
        return redirect(url_for('login'))
    
    # Get all loans for the user
    loans = LoanApplication.query.filter_by(user_id=user.id).order_by(LoanApplication.submitted_at.desc()).all()
    latest_loan = loans[0] if loans else None
    
    # Calculate AI Risk Score
    risk_score = 750  # Default
    ai_score = None
    if latest_loan:
        base_score = latest_loan.credit_score
        # Adjust based on debt-to-income ratio
        if latest_loan.debt_to_income < 0.3:
            risk_score = min(850, base_score + 30)
        elif latest_loan.debt_to_income < 0.4:
            risk_score = base_score
        else:
            risk_score = max(300, base_score - 50)
        ai_score = risk_score
    
    # Mock spending data
    spending = 3240
    
    return render_template('dashboard.html', 
                         user=user, 
                         loans=loans, 
                         latest_loan=latest_loan,
                         risk_score=risk_score,
                         ai_score=ai_score,
                         spending=spending)

# ---------------- LOAN FORM ---------------- 
@app.route('/loan-form', methods=['GET', 'POST'])
def loan_form():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    user = User.query.get(session['user_id'])
    if not user:
        return redirect(url_for('login'))

    if request.method == 'POST':
        try:
            amount = float(request.form.get('amount'))
            income = float(request.form.get('income'))
            credit_score = int(request.form.get('credit_score'))
            employment_years = float(request.form.get('employment_years'))
            debt_to_income = float(request.form.get('debt_to_income'))
            
            if amount < 1000:
                flash('Minimum loan amount is ₹1,000', 'danger')
                return render_template('loan_form.html', user=user)

            # Enhanced loan approval logic
            decision = 'REJECT'
            confidence = 0.0
            rejection_reasons = []
            
            # Rule 1: Credit Score Check (must be at least 300)
            if credit_score < 300:
                rejection_reasons.append(f"Credit score too low ({credit_score}). Minimum required: 300")
            elif credit_score < 500:
                rejection_reasons.append(f"Credit score is borderline ({credit_score}). Recommended: 500+")
            
            # Rule 2: Debt-to-Income Ratio (should be below 0.43)
            if debt_to_income >= 0.43:
                rejection_reasons.append(f"Debt-to-income ratio too high ({debt_to_income*100:.1f}%). Maximum allowed: 43%")
            elif debt_to_income >= 0.36:
                rejection_reasons.append(f"Debt-to-income ratio is high ({debt_to_income*100:.1f}%). Recommended: below 36%")
            
            # Rule 3: Loan-to-Income Ratio (loan shouldn't exceed 3x annual income)
            loan_to_income = amount / income if income > 0 else float('inf')
            if loan_to_income > 3.0:
                rejection_reasons.append(f"Loan amount too high relative to income (₹{amount:,.0f} vs ₹{income:,.0f} annual income)")
            
            # Rule 4: Employment Stability (should have at least 1 year)
            if employment_years < 1:
                rejection_reasons.append(f"Insufficient employment history ({employment_years} years). Minimum: 1 year")
            elif employment_years < 2:
                rejection_reasons.append(f"Limited employment history ({employment_years} years). Recommended: 2+ years")
            
            # Rule 5: Minimum Income Check (should be at least $25,000)
            if income < 25000:
                rejection_reasons.append(f"Income too low (₹{income:,.0f}). Minimum required: ₹25,000")
            
            # Use ML model if available, otherwise use rule-based
            try:
                if ML_AVAILABLE:
                    model = load_model()
                    feature_dict = {
                        'income': income,
                        'credit_score': credit_score,
                        'employment_years': employment_years,
                        'debt_to_income': debt_to_income,
                        'amount': amount
                    }
                    ml_decision, ml_confidence, probs, contributions = predict_single(model, feature_dict)
                    
                    # Combine ML prediction with rule-based checks
                    # Only approve if ML says approve AND all critical rules pass
                    critical_rules_pass = (
                        credit_score >= 300 and
                        debt_to_income < 0.43 and
                        loan_to_income <= 3.0 and
                        employment_years >= 1 and
                        income >= 25000
                    )
                    
                    if ml_decision == 'APPROVE' and critical_rules_pass:
                        # Additional check: credit score should be good for approval
                        # RELAXED: Trust ML model more, but ensure basic sanity
                        if credit_score >= 300:
                            decision = 'APPROVE'
                            confidence = min(ml_confidence, 0.95)
                        else:
                            decision = 'REJECT'
                            confidence = 1.0 - ml_confidence
                            rejection_reasons.append("Credit score below absolute minimum (300)")
                    else:
                        decision = 'REJECT'
                        confidence = 1.0 - ml_confidence
                        if not critical_rules_pass:
                            rejection_reasons.append("Failed critical eligibility checks")
            except Exception as e:
                print(f"ML prediction error: {e}")
                # Fall back to rule-based decision
            
            # Rule-based decision (if ML not used or failed)
            if decision == 'REJECT' and not rejection_reasons:
                # Strict approval criteria
                if (credit_score >= 650 and 
                    debt_to_income < 0.36 and 
                    loan_to_income <= 2.5 and
                    employment_years >= 2 and
                    income >= 30000):
                    decision = 'APPROVE'
                    confidence = 0.85
                elif (credit_score >= 700 and 
                      debt_to_income < 0.30 and 
                      loan_to_income <= 3.0 and
                      employment_years >= 1 and
                      income >= 25000):
                    decision = 'APPROVE'
                    confidence = 0.80
                elif (credit_score >= 300 and 
                      debt_to_income < 0.40 and 
                      loan_to_income <= 2.0 and
                      employment_years >= 1 and
                      income >= 25000):
                    # Tier 3: Modest Approval
                    decision = 'APPROVE'
                    confidence = 0.75
                else:
                    decision = 'REJECT'
                    confidence = 0.70
                    if credit_score < 500:
                        rejection_reasons.append(f"Credit score {credit_score} below minimum threshold (500)")
                    if debt_to_income >= 0.36:
                        rejection_reasons.append(f"Debt-to-income ratio {debt_to_income*100:.1f}% too high (max 36%)")
                    if loan_to_income > 2.5:
                        rejection_reasons.append(f"Loan amount too high relative to income")
                    if employment_years < 2:
                        rejection_reasons.append(f"Employment history too short ({employment_years} years)")
                    if income < 30000:
                        rejection_reasons.append(f"Income too low (₹{income:,.0f})")

            # Store rejection reasons in explanation field
            explanation = None
            if rejection_reasons and decision == 'REJECT':
                explanation = "Reasons: " + "; ".join(rejection_reasons[:3])  # Limit to 3 reasons
            
            loan = LoanApplication(
                user_id=user.id,
                amount=amount,
                income=income,
                credit_score=credit_score,
                employment_years=employment_years,
                debt_to_income=debt_to_income,
                model_decision=decision,
                model_confidence=confidence,
                explanation=explanation,
                submitted_at=datetime.utcnow()
            )
            db.session.add(loan)
            db.session.commit()
            
            if decision == 'APPROVE':
                flash(f'Loan approved! ₹{amount:,.0f} approved with {confidence*100:.0f}% confidence.', 'success')
            else:
                flash(f'Loan application reviewed. Status: {decision}. We will contact you with details.', 'info')
            return redirect(url_for('dashboard'))
        except ValueError as e:
            flash(f'Invalid input: {e}', 'danger')
            return render_template('loan_form.html', user=user)
        except Exception as e:
            flash(f'Error submitting loan: {str(e)}', 'danger')
            return render_template('loan_form.html', user=user)

    return render_template('loan_form.html', user=user)

# ---------------- LOGOUT ---------------- 
@app.route('/logout')
def logout():
    session.pop('user_id', None)
    session.pop('user', None)
    flash('Logged out successfully!', 'success')
    return redirect(url_for('login'))

# ---------------- LOAN HISTORY ---------------- 
@app.route('/loan-history')
def loan_history():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    user = User.query.get(session['user_id'])
    if not user:
        return redirect(url_for('login'))
    
    loans = LoanApplication.query.filter_by(user_id=user.id).order_by(LoanApplication.submitted_at.desc()).all()
    return render_template('loan_history.html', user=user, loans=loans)

# ---------------- LOAN EXPLANATION ---------------- 
@app.route('/loan-explanation')
def loan_explanation():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    user = User.query.get(session['user_id'])
    if not user:
        return redirect(url_for('login'))
    
    loan_id = request.args.get('loan_id')
    if loan_id:
        loan = LoanApplication.query.get(loan_id)
        if loan and loan.user_id == user.id:
            return render_template('loan_explanation.html', user=user, loan=loan)
    
    latest_loan = LoanApplication.query.filter_by(user_id=user.id).order_by(LoanApplication.submitted_at.desc()).first()
    return render_template('loan_explanation.html', user=user, loan=latest_loan)

# ---------------- CONSENT ---------------- 
@app.route('/consent')
def consent():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    user = User.query.get(session['user_id'])
    if not user:
        return redirect(url_for('login'))
    
    return render_template('consent.html', user=user)

# ---------------- PROFILE ---------------- 
@app.route('/profile')
def profile():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    user = User.query.get(session['user_id'])
    if not user:
        return redirect(url_for('login'))
    
    return render_template('profile.html', user=user)

# ---------------- ROOT ---------------- 
@app.route('/')
def index():
    if 'user_id' in session:
        return redirect(url_for('dashboard'))
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)
