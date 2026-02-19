from config import *
import os
import pandas as pd
from datetime import datetime
from dateutil.relativedelta import relativedelta
import calendar
from support import *



current_path = os.getcwd() + '/'

mode = input('USER or AUTO: ').upper()
if mode == 'USER':
    #user Input
    loan_amount_input = input('Enter Loan Amount (in numbers): ')
    loan_interest_rate_input = input('Enter Annual Interest Rate (in %):')
    loan_tenure_input = input('Enter Loan Tenure (in Months): ')
    loan_start_input = input('Enter Loan start date (eg FEB-26): ').upper()
    lum_sum_amount_input = input('Enter Lum Sum amount invested (in numbers): ')

else:
    loan_amount_input = LOAN_AMT
    loan_interest_rate_input = INTEREST_RATE
    loan_tenure_input = TENURE_IN_MONTH
    loan_start_input = LOAN_START_DATE
    lum_sum_amount_input = LUMSUM_AMT


loan_amount = float(loan_amount_input)
loan_tenure = float(loan_tenure_input)/12
loan_interest_rate = float(loan_interest_rate_input)/100
loan_start_date = datetime.strptime(loan_start_input, "%b-%y")
lum_sum_amount = float(lum_sum_amount_input)

############################
#calculation Monthly EMI
############################

fixed_monthly_payment = monthly_emi(loan_amount,loan_interest_rate,loan_tenure)
print('Your Monthly EMI:',round(fixed_monthly_payment))