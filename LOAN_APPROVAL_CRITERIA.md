# Loan Approval Criteria

## Approval Requirements

A loan application will be **APPROVED** only if ALL of the following criteria are met:

### Critical Requirements (All Must Pass):
1. **Credit Score**: Minimum 300 (500+ recommended)
2. **Debt-to-Income Ratio**: Below 43% (36% or lower recommended)
3. **Loan-to-Income Ratio**: Loan amount ≤ 3x annual income
4. **Employment History**: Minimum 1 year (2+ years recommended)
5. **Minimum Income**: At least ₹25,000 annually (₹30,000+ recommended)

### Approval Tiers:

**Tier 1 - Excellent (High Confidence ~85-95%)**
- Credit Score: 650+
- Debt-to-Income: < 36%
- Loan-to-Income: ≤ 2.5x
- Employment: 2+ years
- Income: ₹30,000+

**Tier 2 - Good (Moderate Confidence ~80%)**
- Credit Score: 700+
- Debt-to-Income: < 30%
- Loan-to-Income: ≤ 3.0x
- Employment: 1+ years
- Income: ₹25,000+

**Tier 3 - Borderline (Lower Confidence ~70-75%)**
- Credit Score: 620-649
- Debt-to-Income: < 30%
- Other factors must be strong

### Automatic Rejection Reasons:
- Credit Score < 300
- Debt-to-Income ≥ 43%
- Loan amount > 3x annual income
- Employment < 1 year
- Annual income < ₹25,000

## Examples

### ✅ Will Approve:
- Credit: 720, Income: ₹60,000, DTI: 25%, Loan: ₹50,000, Employment: 5 years
- Credit: 680, Income: ₹45,000, DTI: 30%, Loan: ₹30,000, Employment: 3 years

### ❌ Will Reject:
- Credit: 250, Income: ₹40,000, DTI: 35%, Loan: ₹50,000, Employment: 2 years
- Credit: 650, Income: ₹20,000, DTI: 40%, Loan: ₹40,000, Employment: 1 year

