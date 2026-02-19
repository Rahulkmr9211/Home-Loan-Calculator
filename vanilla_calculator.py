from config import *
import os
import pandas as pd

current_path = os.getcwd() + '/'

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
fixed_monthly_payment = (loan_amount * monthly_interest_rate * ((1.0+monthly_interest_rate)**total_payments_count))/(((1.0+monthly_interest_rate)**total_payments_count)-1)
print('Your Monthly EMI:',round(fixed_monthly_payment))

#Month-on-Month Amortization
amortization_df = pd.DataFrame(columns=['MONTH','OPENING_BALANCE','EMI','INTEREST','PRINCIPAL','CLOSING_BALANCE'],index=[i for i in range(loan_tenure_input)])
amortization_df['EMI'] = fixed_monthly_payment
for i in range(loan_tenure_input):
    amortization_df.loc[i,'MONTH'] = i+1
    if i == 0:
        amortization_df.loc[i,'OPENING_BALANCE'] = loan_amount
    else:
        amortization_df.loc[i,'OPENING_BALANCE'] = amortization_df.loc[i-1,'CLOSING_BALANCE']
    amortization_df.loc[i,'INTEREST'] = amortization_df.loc[i,'OPENING_BALANCE']*monthly_interest_rate
    amortization_df.loc[i,'PRINCIPAL'] = amortization_df.loc[i,'EMI'] - amortization_df.loc[i,'INTEREST']
    amortization_df.loc[i,'CLOSING_BALANCE'] = amortization_df.loc[i,'OPENING_BALANCE'] - amortization_df.loc[i,'PRINCIPAL']

mom_amortization_df = amortization_df.copy()
    



