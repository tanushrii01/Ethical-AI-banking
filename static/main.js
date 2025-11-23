// ==================== DATA STORE ====================
let currentUser = null;
let consentSettings = {
    income: true,
    location: true,
    demographics: true,
    spending: true,
    credit: true
};

// ==================== USER MANAGEMENT ====================
function saveUserToStorage(user) {
    localStorage.setItem('currentUser', JSON.stringify(user));
}

function loadUserFromStorage() {
    const userData = localStorage.getItem('currentUser');
    if (userData) {
        currentUser = JSON.parse(userData);
        return currentUser;
    }
    return null;
}

function getUserInitials(name) {
    if (!name) return 'U';
    const parts = name.trim().split(' ');
    if (parts.length >= 2) {
        return (parts[0][0] + parts[parts.length - 1][0]).toUpperCase();
    }
    return name.substring(0, 2).toUpperCase();
}

// ==================== LOGIN FUNCTIONS ====================
function login() {
    const email = document.getElementById('loginEmail').value.trim();
    const password = document.getElementById('loginPassword').value;
    const fullName = document.getElementById('loginName').value.trim();
    const loanAmount = document.getElementById('loanAmount').value.trim();

    // Validation
    if (!email) {
        showNotification('❌ Please enter your email', 'danger');
        return;
    }
    if (!password) {
        showNotification('❌ Please enter your password', 'danger');
        return;
    }
    if (!fullName) {
        showNotification('❌ Please enter your full name', 'danger');
        return;
    }
    if (!loanAmount || isNaN(loanAmount) || parseFloat(loanAmount) <= 0) {
        showNotification('❌ Please enter a valid loan amount', 'danger');
        return;
    }

    // Create user object
    currentUser = {
        name: fullName,
        email: email,
        type: 'customer',
        loanAmount: parseFloat(loanAmount),
        loginTime: new Date().toISOString()
    };

    // Save to localStorage
    saveUserToStorage(currentUser);

    // Redirect to dashboard
    showNotification('✅ Login successful! Welcome ' + fullName);
    setTimeout(() => {
        window.location.href = '/dashboard';
    }, 1000);
}

function loginAsAdmin() {
    // Admin credentials
    const adminEmail = 'admin@trustbank.com';
    const adminPassword = 'admin123';

    currentUser = {
        name: 'Admin User',
        email: adminEmail,
        type: 'admin',
        loginTime: new Date().toISOString()
    };

    // Save to localStorage
    saveUserToStorage(currentUser);

    // Redirect to governance dashboard
    showNotification('✅ Admin login successful!');
    setTimeout(() => {
        window.location.href = '/governance';
    }, 1000);
}

function logout() {
    currentUser = null;
    localStorage.removeItem('currentUser');
    showNotification('✅ Logged out successfully');
    setTimeout(() => {
        window.location.href = '/logout';
    }, 1000);
}

function showForgotPassword() {
    showNotification('📧 Password reset link sent to your email!');
}

// ==================== PAGE INITIALIZATION ====================
function initializePage() {
    // Only run client-side auth checks if we're NOT on login/signup pages
    // Flask handles authentication server-side
    const currentPath = window.location.pathname;
    if (currentPath === '/login' || currentPath === '/signup') {
        // Don't interfere with login/signup forms
        return;
    }
    
    const user = loadUserFromStorage();
    
    if (!user) {
        // Only redirect if we're on a protected page
        // Let Flask handle authentication redirects
        return;
    }

    currentUser = user;

    // Update user info in header if exists
    const userNameElement = document.getElementById('userName');
    const userAvatarElement = document.getElementById('userAvatar');

    if (userNameElement) {
        userNameElement.textContent = user.name;
    }

    if (userAvatarElement) {
        userAvatarElement.textContent = getUserInitials(user.name);
    }

    // Update loan amount display if on dashboard or loan explanation page
    if (user.loanAmount) {
        updateLoanDisplay(user.loanAmount);
    }
}

function updateLoanDisplay(amount) {
    // Format loan amount with commas
    const formattedAmount = '₹' + amount.toLocaleString('en-US', {
        minimumFractionDigits: 0,
        maximumFractionDigits: 0
    });

    // Update dashboard loan amount
    const loanAmountElements = document.querySelectorAll('.loan-amount');
    loanAmountElements.forEach(el => {
        el.textContent = formattedAmount;
    });

    // Update loan status text
    const loanStatusElements = document.querySelectorAll('.loan-status-text');
    loanStatusElements.forEach(el => {
        el.textContent = `${formattedAmount} Credit Line`;
    });
}

// ==================== CONSENT PAGE ====================
function updateConsent(category, enabled) {
    consentSettings[category] = enabled;
    updateConsentImpact();
}

function updateConsentImpact() {
    const enabledCount = Object.values(consentSettings).filter(v => v).length;
    const impactDiv = document.getElementById('consentImpact');
    
    if (!impactDiv) return;
    
    if (enabledCount === 5) {
        impactDiv.className = 'alert alert-success';
        impactDiv.innerHTML = '✅ All data categories enabled. AI will have maximum accuracy in decisions.';
    } else if (enabledCount >= 3) {
        impactDiv.className = 'alert alert-warning';
        impactDiv.innerHTML = `⚠️ ${5 - enabledCount} categories disabled. AI accuracy may be slightly reduced.`;
    } else {
        impactDiv.className = 'alert alert-danger';
        impactDiv.innerHTML = `❌ Only ${enabledCount} categories enabled. AI decisions may be significantly less accurate.`;
    }
}

function saveConsent() {
    localStorage.setItem('consentSettings', JSON.stringify(consentSettings));
    showNotification('✅ Consent preferences saved successfully!');
}

// Load consent settings
function loadConsentSettings() {
    const savedConsent = localStorage.getItem('consentSettings');
    if (savedConsent) {
        consentSettings = JSON.parse(savedConsent);
        
        // Update checkboxes
        Object.keys(consentSettings).forEach(key => {
            const checkbox = document.querySelector(`input[onchange*="${key}"]`);
            if (checkbox) {
                checkbox.checked = consentSettings[key];
            }
        });
    }
}

// ==================== PROFILE PAGE ====================
function requestCorrection(field) {
    const user = loadUserFromStorage();
    showNotification(`📝 Correction request submitted for ${field}. Our team will review within 2 business days.`);
    
    // Log correction request
    console.log(`Correction requested for ${field} by ${user ? user.name : 'Unknown'}`);
}

// ==================== ADMIN FUNCTIONS ====================
function downloadReport() {
    showNotification('📥 Downloading comprehensive AI governance report...');
    setTimeout(() => {
        showNotification('✅ Report downloaded successfully!');
    }, 1500);
}

function reviewCase(caseId) {
    const reviewDetail = document.getElementById('reviewDetail');
    if (!reviewDetail) return;
    
    reviewDetail.style.display = 'block';
    document.getElementById('reviewCaseId').textContent = caseId;
    
    const customers = {
        8492: 'John Smith',
        8493: 'Sarah Johnson',
        8494: 'Mike Davis'
    };
    
    document.getElementById('reviewCustomerName').textContent = customers[caseId] || 'Unknown';
    
    // Scroll to review detail
    setTimeout(() => {
        reviewDetail.scrollIntoView({ behavior: 'smooth', block: 'start' });
    }, 100);
}

function closeReview() {
    const reviewDetail = document.getElementById('reviewDetail');
    if (reviewDetail) {
        reviewDetail.style.display = 'none';
    }
}

function approveDecision() {
    const notes = document.getElementById('reviewNotes').value.trim();
    if (!notes) {
        showNotification('⚠️ Please add review notes before approving', 'warning');
        return;
    }
    showNotification('✅ AI decision approved. Case moved to completed reviews.');
    closeReview();
    setTimeout(() => {
        window.location.href = '/governance';
    }, 1500);
}

function overrideDecision() {
    const notes = document.getElementById('reviewNotes').value.trim();
    if (!notes) {
        showNotification('⚠️ Please add review notes explaining the override', 'warning');
        return;
    }
    showNotification('✅ Decision overridden. Customer will be notified of the new decision.');
    closeReview();
    setTimeout(() => {
        window.location.href = '/governance';
    }, 1500);
}

function requestMoreInfo() {
    showNotification('📋 Information request sent to customer. Case status: Pending additional info.');
    closeReview();
}

// ==================== ERROR PAGE ====================
function retryAction() {
    showNotification('🔄 Retrying...');
    setTimeout(() => {
        showNotification('✅ Action completed successfully!');
        window.location.href = '/dashboard';
    }, 1500);
}

function contactSupport() {
    const user = loadUserFromStorage();
    const caseId = document.getElementById('errorCaseId') ? document.getElementById('errorCaseId').textContent : '#UNKNOWN';
    showNotification(`📞 Support ticket created with Case ID ${caseId}. Our team will contact you within 24 hours.`);
    
    console.log(`Support ticket created for ${user ? user.name : 'Unknown'} - Case ${caseId}`);
}

// ==================== NAVIGATION ====================
function navigateTo(page) {
    // Convert .html to Flask routes
    const routeMap = {
        'dashboard.html': '/dashboard',
        'login.html': '/login',
        'signup.html': '/signup',
        'governance.html': '/governance',
        'loan-form.html': '/loan-form',
        'loan-history.html': '/loan-history',
        'loan-explanation.html': '/loan-explanation',
        'profile.html': '/profile',
        'consent.html': '/consent'
    };
    const route = routeMap[page] || page;
    window.location.href = route;
}

// ==================== NOTIFICATIONS ====================
function showNotification(message, type = 'success') {
    const notification = document.createElement('div');
    notification.className = 'notification';
    
    const colors = {
        success: 'var(--success)',
        danger: 'var(--danger)',
        warning: 'var(--warning)',
        info: 'var(--primary)'
    };
    
    notification.style.borderLeft = `4px solid ${colors[type] || colors.success}`;
    notification.innerHTML = `<div style="font-weight: 500;">${message}</div>`;
    
    document.body.appendChild(notification);

    setTimeout(() => {
        notification.remove();
    }, 3000);
}

// ==================== INITIALIZE ON PAGE LOAD ====================
document.addEventListener('DOMContentLoaded', () => {
    console.log('Ethical AI Banking Platform Loaded');
    
    // Don't run initializePage on login/signup pages - let Flask handle them
    const currentPath = window.location.pathname;
    if (currentPath !== '/login' && currentPath !== '/signup') {
        // Initialize page with user data
        initializePage();
    }
    
    // Load consent settings if on consent page
    if (document.getElementById('consentImpact')) {
        loadConsentSettings();
        updateConsentImpact();
    }
});