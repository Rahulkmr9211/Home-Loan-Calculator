

def monthly_emi(loan_amount,loan_interest_rate,loan_tenure):
    monthly_interest_rate = loan_interest_rate / 12
    total_payments_count = loan_tenure * 12
    fixed_monthly_payment = (loan_amount * monthly_interest_rate * ((1.0+monthly_interest_rate)**total_payments_count))/(((1.0+monthly_interest_rate)**total_payments_count)-1)
    return fixed_monthly_payment
