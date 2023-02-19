from datetime import date
from customer import Customer
import random
import numpy as np
from dateutil.relativedelta import relativedelta
import uuid

PAST_DATE = date.today() - relativedelta(years=2)
PURPOSES = ['car', 'education', 'vacation', 'business', 'other']
DEPT_TO_INCOME_RATIO = 0.6
MONTH_IN_YEAR = 12


class Loan:

    def __init__(self, customer: Customer, slice_from_beginning: int, slice_from_new_date: int):
        self.slice_from_beginning = slice_from_beginning
        self.slice_from_new_date = slice_from_new_date

        self.date = self.generate_date()
        self.customer = customer
        self.customer_id = self.customer.customer_id
        self.loan_id = str(uuid.uuid3(uuid.NAMESPACE_X500, self.customer_id + str(self.date)))
        self.loan_type = random.choice(PURPOSES)
        self.loan_length = 3
        self.interest_rate = 0.0499
        self.generate_loan_size()
        self.loan_size = self.generate_loan_size()
        self.full_dept = 0
        self.loan_month_payment = self.calculate_loan_month_payment()

        self.customer.borrowing_capacity = self.calculate_borrowing_capacity()

    def generate_loan_size(self) -> int:
        """
        This function generates a random loan size based on the loan type.
        :return: int: A random loan size based on the loan type.
        """
        if self.loan_type == 'car':
            loan_size = random.choice(np.arange(50_000, 710_000, 10_000))
            self.loan_length = 5
        elif self.loan_type == 'education':
            loan_size = random.choice(np.arange(20_000, 200_000, 5_000))
        elif self.loan_type == 'vacation':
            loan_size = random.choice(np.arange(5_000, 20_000, 1_000))
        elif self.loan_type == 'business':
            loan_size = random.choice(np.arange(50_000, 200_000, 5_000))
        else:
            loan_size = random.choice(np.arange(5_000, 100_000, 1_000))

        if loan_size < 10_000:
            self.loan_length = 1

        return loan_size

    def generate_date(self):
        """
        Function that generates a random date within a chosen range.
        :return: a randomly generated date.
        """
        random_num_days = random.randint(0, self.slice_from_new_date)
        return PAST_DATE + relativedelta(days=self.slice_from_beginning) + relativedelta(days=random_num_days)

    def calculate_loan_month_payment(self):
        """
        Calculates the monthly payment for a loan based on the simple interest formula.
        I = P * r * T, where
        I - simple interest,
        P - principal amount,
        r - interest rate
        T - time involved
        loan_month_payment = (P + I) / (T * 12)
        :return: loan_month_payment
        """
        self.full_dept = self.loan_size + self.loan_size * self.interest_rate * self.loan_length
        return self.full_dept / (self.loan_length * MONTH_IN_YEAR)

    def calculate_borrowing_capacity(self) -> float:
        """
        Calculate the maximum amount that a client can borrow based on their income, debt-to-income ratio, and other monthly debt payments.

        debt_to_income_ratio (float): Maximum debt-to-income ratio allowed by the lender
        other_debt_payments (float): Monthly debt payments other than the proposed loan (optional, default=0)

        :return: float: Maximum loan amount that the client can borrow
        """
        # Calculate the maximum monthly debt payment based on the debt-to-income ratio
        max_monthly_debt_payment = self.customer.month_income * DEPT_TO_INCOME_RATIO

        # Calculate the maximum monthly loan payment as 30% of the client's monthly income
        max_monthly_loan_payment = self.customer.month_income * 0.3

        # Subtract any other monthly debt payments from the maximum monthly debt payment
        net_monthly_debt_payment = max_monthly_debt_payment - sum(self.customer.total_current_debt)

        # Calculate the monthly interest rate and number of payments
        monthly_interest_rate = self.interest_rate / MONTH_IN_YEAR
        num_payments = self.loan_length * MONTH_IN_YEAR

        # Calculate the maximum loan amount that the client can borrow based on the net monthly debt payment, the maximum monthly loan payment, and the loan terms
        max_loan_amount = (net_monthly_debt_payment - max_monthly_loan_payment) * (
                (1 - (1 + monthly_interest_rate) ** -num_payments) / monthly_interest_rate)

        return max_loan_amount

    def can_take_loan(self, credit_score_threshold, debt_to_income_ratio):
        """
        Checks if the customer is eligible for a loan based on their credit score,
        debt-to-income ratio, and borrowing capacity.

        :param credit_score_threshold: The minimum credit score required to be eligible for a loan
        :param debt_to_income_ratio: The maximum debt-to-income ratio allowed to be eligible for a loan
        :return: True if the customer is eligible for the loan, False otherwise
        """
        # Check if client's credit score meets the minimum requirement
        if self.customer.credit_score < credit_score_threshold:
            return False

        # Calculate the client's debt-to-income ratio
        total_current_debt = sum(self.customer.total_current_debt)
        debt_ratio = total_current_debt / self.customer.month_income

        # Check if the client's debt-to-income ratio is below the threshold
        if debt_ratio >= debt_to_income_ratio:
            return False

        # Check if loan size is within borrowing capacity
        if self.full_dept > self.customer.borrowing_capacity:
            return False

        # If all conditions are met, the client can take the loan
        return True

    def create_ds_row(self):
        """
        Creates a dictionary containing the data for a single loan to be added to the data store.

        :return: A dictionary representing the loan data
        """
        return {
            'loan_id': self.loan_id,
            'customer_id': self.customer_id,
            'date': self.date,
            'loan_size': self.loan_size,
            'loan_type': self.loan_type
        }
