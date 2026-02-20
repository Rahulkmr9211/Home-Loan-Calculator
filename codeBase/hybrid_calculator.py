from config import *
import os
import pandas as pd
from datetime import datetime
from dateutil.relativedelta import relativedelta
import calendar
from codeBase.support import *
import ast



current_path = os.getcwd() + '/'

mode = input('USER or AUTO: ').upper()
if mode == 'USER':
    #user Input
    loan_amount_input = input('Enter Loan Amount (in numbers): ')
    loan_interest_rate_input = input('Enter Annual Interest Rate (in %):')
    loan_tenure_input = input('Enter Loan Tenure (in Months): ')
    loan_start_input = input('Enter Loan start date (eg FEB-26): ').upper()
    lum_sum_amount_input = input('Enter Lum Sum amount invested (in [numbers]): ')
    lum_sum_date_input = input('Enter Lum Sum invested date (eg [FEB-26]): ')
    regular_amount_input = input('Enter Extra amount invested (in numbers): ')
    payment_months_input = input('Enter payment month number list (eg [1,2] max 12): ')
    regular_payment_start_date_input = input('Enter Loan start date (eg FEB-26): ').upper()

else:
    loan_amount_input = LOAN_AMT
    loan_interest_rate_input = INTEREST_RATE
    loan_tenure_input = TENURE_IN_MONTH
    loan_start_input = LOAN_START_DATE
    lum_sum_amount_input = LUMSUM_AMT
    lum_sum_date_input = LUMSUM_AMT_DATE
    regular_amount_input = REGULAR_AMT
    payment_months_input = REULAR_MONTHS
    regular_payment_start_date_input = REGULAR_PAYMENT_START_DATE

loan_tenure_input = int(loan_tenure_input)
loan_amount = float(loan_amount_input)
loan_tenure = loan_tenure_input/12
loan_interest_rate = float(loan_interest_rate_input)/100
loan_start_date = datetime.strptime(loan_start_input, "%b-%y")
#lumpsum
lum_sum_amount = ast.literal_eval(lum_sum_amount_input)
lum_sum_date = ast.literal_eval(lum_sum_date_input)
lum_sum_date = [datetime.strptime(i.upper(), "%b-%y") for i in lum_sum_date]
lum_sum_detail_dict = dict(zip(lum_sum_date, lum_sum_amount))
#regular-interval
regular_amount = float(regular_amount_input)
payment_months = ast.literal_eval(payment_months_input)
regular_payment_start_date = datetime.strptime(regular_payment_start_date_input, "%b-%y")

############################
#calculation Monthly EMI
############################

monthly_interest_rate, fixed_monthly_payment = monthly_emi(loan_amount,loan_interest_rate,loan_tenure)
print('Your Monthly EMI:',round(fixed_monthly_payment))

##############################
#Month-on-Month Amortization
##############################
amortization_df = pd.DataFrame(columns=['MONTH','YEAR','OPENING_BALANCE','EMI','INTEREST','PRINCIPAL','CLOSING_BALANCE'],index=[i for i in range(loan_tenure_input)])
amortization_df['EMI'] = round(fixed_monthly_payment)
for i in range(loan_tenure_input):
    if i == 0:
        loan_date_itr = loan_start_date
        amortization_df.loc[i,'OPENING_BALANCE'] = round(loan_amount)
    else:
        loan_date_itr = loan_start_date + relativedelta(months=i)
        amortization_df.loc[i,'OPENING_BALANCE'] = amortization_df.loc[i-1,'CLOSING_BALANCE']
    
    month_number = loan_date_itr.month
    year = loan_date_itr.year
    amortization_df.loc[i,'MONTH'] = calendar.month_name[month_number]
    amortization_df.loc[i,'YEAR'] = year

    amortization_df.loc[i,'INTEREST'] = round(amortization_df.loc[i,'OPENING_BALANCE']*monthly_interest_rate)
    amortization_df.loc[i,'PRINCIPAL'] = round(amortization_df.loc[i,'EMI'] - amortization_df.loc[i,'INTEREST'])

    if loan_date_itr in lum_sum_detail_dict.keys():
        amortization_df.loc[i,'PRINCIPAL'] = round(amortization_df.loc[i,'PRINCIPAL'] + lum_sum_detail_dict[loan_date_itr])
    
    if (month_number in payment_months) & (loan_date_itr >= regular_payment_start_date):
        amortization_df.loc[i,'PRINCIPAL'] = round(amortization_df.loc[i,'PRINCIPAL']+regular_amount)
    
    amortization_df.loc[i,'CLOSING_BALANCE'] = round(amortization_df.loc[i,'OPENING_BALANCE'] - amortization_df.loc[i,'PRINCIPAL'])

    if amortization_df.loc[i,'CLOSING_BALANCE'] <= 0:
        break
    
    

amortization_df.dropna(how='any',inplace=True)
mom_amortization_df = amortization_df.copy()

##############################
#Year-on-Year Amortization
##############################
yoy_amortization_df = YOY_amortization_calculation(mom_amortization_df)

#############################
#SUMMARY
#############################
summary_dict = {'TOTAL LOAN AMOUNT':loan_amount,
                'INTEREST RATE':loan_interest_rate*100,
                'ORIGINAL TENURE IN MONTHS':loan_tenure*12,
                'REVISED TENURE IN MONTHS':len(mom_amortization_df)-1,
                'REGULAR AMOUNT PAY':regular_amount,
                'LUMSUM AMOUNT PAY':sum(lum_sum_amount),
                'LOAN START DATE':loan_start_input,
                'ORIGINAL LOAN END DATE':(loan_start_date + relativedelta(months=loan_tenure_input-1)).strftime(format='%b-%Y').upper(),
                'REVISED LOAN END DATE':loan_date_itr.strftime(format='%b-%Y').upper(),
                'MONTHLY EMI':round(fixed_monthly_payment),
                'TOTAL INTEREST PAY':yoy_amortization_df['INTEREST'].sum(),
                'TOTAL AMOUNT PAY':yoy_amortization_df['INTEREST'].sum()+loan_amount}


summary_df = pd.DataFrame(columns=['KEY','VALUE'],index=[i for i in range(len(summary_dict.keys()))])

for i, key_value in enumerate(summary_dict.keys()):
    summary_df.loc[i,'KEY'] = key_value
    summary_df.loc[i,'VALUE'] = summary_dict[key_value]

print(summary_df)
print('Saving Excel File')
os.makedirs(current_path+'Output', exist_ok=True)
with pd.ExcelWriter(current_path+"Output/HYBRID BASED AMORTIZATION.xlsx", engine="xlsxwriter") as writer:
    summary_df.to_excel(writer, sheet_name="Summary", index=False)
    yoy_amortization_df.to_excel(writer, sheet_name="YOY", index=False)
    mom_amortization_df.to_excel(writer, sheet_name="MOM", index=False)