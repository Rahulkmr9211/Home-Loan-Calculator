from config import *

mode = input('USER or AUTO: ').upper()
if mode == 'USER':
    #user Input
    loan_amount_input = input('Enter Loan Amount (in numbers): ')
    loan_interest_rate_input = input('Enter Annual Interest Rate (in %):')
    loan_tenure_input = input('Enter Loan Tenure (in Months): ')
else:
    loan_amount_input = LOAN_AMT
    loan_interest_rate_input = INTEREST_RATE
    loan_tenure_input = TENURE_IN_MONTH


loan_amount = float(loan_amount_input)
loan_tenure = float(loan_tenure_input)/12
loan_interest_rate = float(loan_interest_rate_input)/100

#calculation Monthly EMI
monthly_interest_rate = loan_interest_rate / 12
total_payments_count = loan_tenure * 12
fixed_monthly_payment = (loan_amount * monthly_interest_rate * ((1.0+monthly_interest_rate)**total_payments_count))/(((1.0+monthly_interest_rate)**total_payments_count)-1) + 34
print('Your Monthly EMI:',round(fixed_monthly_payment))


