# TrustBank AI - Setup Instructions

## Quick Start

1. **Open Terminal in VS Code** (Terminal → New Terminal)

2. **Navigate to project folder:**
   ```bash
   cd Ethical-AI-banking
   ```

3. **Install dependencies (if not already installed):**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the application:**
   ```bash
   python app.py
   ```
   
   OR use the run script:
   ```bash
   python run.py
   ```

5. **Open your browser:**
   - Go to: `http://127.0.0.1:5000`
   - Or: `http://localhost:5000`

## Default Login Credentials

**Admin Account:**
- Email: `admin@trustbank.com`
- Password: `admin123`

## Create New Account

1. Go to `http://127.0.0.1:5000/signup`
2. Fill in your details
3. You'll be automatically logged in

## Troubleshooting

### 404 Error
- Make sure the Flask app is running (check terminal)
- Make sure you're accessing `http://127.0.0.1:5000` (not just `127.0.0.1:5000`)
- Check if port 5000 is already in use

### Database Error
- The database will be created automatically at `instance/app.sqlite`
- If you get database errors, delete `instance/app.sqlite` and restart the app

### Import Errors
- Make sure all dependencies are installed: `pip install -r requirements.txt`
- Make sure you're in the `Ethical-AI-banking` directory when running

## Available Routes

- `/` - Root (redirects to login or dashboard)
- `/login` - Login page
- `/signup` - Signup page
- `/dashboard` - User dashboard
- `/loan-form` - Apply for a loan
- `/loan-history` - View loan history
- `/loan-explanation` - View loan decision explanation
- `/profile` - User profile
- `/consent` - Data consent settings
- `/logout` - Logout

## Project Structure

```
Ethical-AI-banking/
├── app.py              # Main Flask application
├── models.py           # Database models
├── ml.py              # ML model functions
├── run.py             # Run script
├── requirements.txt   # Python dependencies
├── instance/
│   └── app.sqlite     # SQLite database (auto-created)
├── static/
│   ├── style.css      # Styles
│   └── main.js        # JavaScript
└── templates/
    └── *.html         # HTML templates
```

