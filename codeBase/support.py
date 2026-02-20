import math
import pandas as pd

def monthly_emi(loan_amount,loan_interest_rate,loan_tenure):
    monthly_interest_rate = loan_interest_rate / 12
    total_payments_count = loan_tenure * 12
    fixed_monthly_payment = (loan_amount * monthly_interest_rate * ((1.0+monthly_interest_rate)**total_payments_count))/(((1.0+monthly_interest_rate)**total_payments_count)-1)
    return monthly_interest_rate, fixed_monthly_payment

def YOY_amortization_calculation(mom_amortization_df):
    amortization_df = mom_amortization_df.groupby('YEAR')[['EMI','INTEREST','PRINCIPAL']].sum().reset_index()
    temp = mom_amortization_df[['YEAR','OPENING_BALANCE']].drop_duplicates(keep='first',subset='YEAR')
    amortization_df = pd.merge(amortization_df,temp,on='YEAR',how='left')
    temp = mom_amortization_df[['YEAR','CLOSING_BALANCE']].drop_duplicates(keep='last',subset='YEAR')
    amortization_df = pd.merge(amortization_df,temp,on='YEAR',how='left')
    amortization_df = amortization_df[['YEAR','OPENING_BALANCE','EMI','INTEREST','PRINCIPAL','CLOSING_BALANCE']]
    return amortization_df

class lum_sum:
    def revised_tenure(fixed_monthly_payment,revised_principal,monthly_interest_rate):
        numerator = math.log(fixed_monthly_payment/(fixed_monthly_payment - revised_principal*monthly_interest_rate))
        denominator = math.log(1+monthly_interest_rate)
        loan_tenure = numerator/denominator
        return loan_tenure
