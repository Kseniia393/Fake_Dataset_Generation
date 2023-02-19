import pandas as pd
import numpy as np
from customer import Customer
from loan import Loan
from datetime import date
from dateutil.relativedelta import relativedelta
from tqdm import tqdm
import random
import argparse

MINIMUM_WAGE = 6000


def main():
    # Number of clients
    parser = argparse.ArgumentParser()
    parser.add_argument('-n', "--num_clients", default=1000, help='Enter number of clients that you wanna see in dataset.')
    args = parser.parse_args()
    num_clients = int(args.num_clients)

    # Generate N clients
    customers = [Customer() for _ in tqdm(range(num_clients))]

    # Lists for future datasets
    per_client_per_day = []
    loans_table = []

    for customer in tqdm(customers):
        last_date = customer.timestamp
        date_of_birth = customer.date_of_birth

        # Generate N loans for client
        num_loans = np.random.choice(a=np.arange(3, 7))
        loans = [Loan(customer, random.randint(0, 90), random.randint(300, 640)) for _ in range(num_loans)]
        while last_date < date.today() - relativedelta(days=1):

            last_date = customer.timestamp
            # update age on a current date
            customer.age = last_date.year - date_of_birth.year - (
                    (last_date.month, last_date.day) < (date_of_birth.month, date_of_birth.day))
            for loan in loans:
                if loan.date == last_date:
                    if loan.can_take_loan(670, 0.4):
                        customer.num_current_loans += 1
                        customer.total_current_debt.append(loan.full_dept)
                        customer.total_loans_amount.append(loan.loan_size)
                        customer.loans_repayment = 0
                        customer.loans_month_payment.append(loan.loan_month_payment)
                        loans_table.append(loan.create_ds_row())

            # Simulate salary day
            if last_date.day == 1:
                customer.current_balance += customer.month_income

            # day when all expenses deducted
            elif last_date.day == 10:
                if customer.residential_status == 'owns':
                    customer.monthly_expenses = np.random.choice(np.arange(0.3, 0.5, 0.05))
                else:
                    customer.monthly_expenses = np.random.choice(np.arange(0.4, 0.65, 0.05))
                customer.current_balance -= max(customer.monthly_expenses * customer.current_balance, MINIMUM_WAGE)

            # Simulate loan payment day
            elif last_date.day == 15:
                # Check if the client can pay loan on current date
                for i, loan_month_payment in enumerate(customer.loans_month_payment):
                    if round(customer.total_current_debt[i], 2) > 0:
                        if customer.current_balance - loan_month_payment > 0:
                            customer.loans_repayment += loan_month_payment
                            customer.total_current_debt[i] -= loan_month_payment
                            customer.current_balance -= loan_month_payment
                        else:
                            customer.payment_history += 1
                            customer.credit_score -= 10
                    else:
                        customer.total_current_debt.pop(i)
                        customer.loans_month_payment.pop(i)
                        customer.total_loans_amount.pop(i)
                        customer.num_current_loans -= 1

            # Add savings
            elif last_date.day == 17:
                if customer.savings > 0:
                    new_savings = random.randint(500, 2000)
                    if customer.current_balance > new_savings:
                        customer.savings += new_savings
                        customer.current_balance -= new_savings

            # Add investments
            elif last_date.day == 19:
                if customer.investment > 0:
                    new_investments = random.randint(500, 4000)
                    if customer.current_balance > new_investments:
                        customer.investment += new_investments
                        customer.current_balance -= new_investments

            elif last_date.day == 25:
                customer.savings += customer.savings * 0.01

            elif last_date.day == 30:
                monthly_return = random.uniform(-0.1, 0.1) * customer.investment
                customer.investment += monthly_return

            else:
                customer.loans_repayment = 0
                customer.monthly_expenses = 0

            customer.current_balance = customer.current_balance
            customer.total_current_debt = customer.total_current_debt
            customer.timestamp = last_date + relativedelta(days=1)
            per_client_per_day.append(customer.create_ds_row())

    per_client_per_day_df = pd.DataFrame(per_client_per_day)
    loans_table_df = pd.DataFrame(loans_table)

    per_client_per_day_df.to_csv('per_client_per_day.csv')
    loans_table_df.to_csv('loans_table.csv')


if __name__ == "__main__":
    main()
