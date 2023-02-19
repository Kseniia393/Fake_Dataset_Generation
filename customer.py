from datetime import date
from dateutil.relativedelta import relativedelta
from faker import Faker
import random
import numpy as np
import uuid

GENDERS = ['male', 'female']
EMPLOYMENT_STATUSES = ['full-time', 'part-time', 'self-employed']
"""Assume that client at least finished the school"""
EDUCATION_LEVELS = ['HS-grad', 'Some-college', 'Bachelors', 'Masters', 'Doctorate']
MARITAL_STATUSES = ['married', 'single', 'divorced', 'widowed']
PAST_DATE = date.today() - relativedelta(years=2)
RESIDENTIAL_STATUS = ['owns', 'rent']


class Customer:
    """A class to represent a bank customer."""
    def __init__(self):
        self.timestamp = PAST_DATE
        self.customer_id = str(uuid.uuid4())

        self.date_of_birth = self.generate_date_of_birth()
        self.age = self.calculate_age(PAST_DATE)
        self.gender = np.random.choice(GENDERS, p=[0.51, 0.49])
        self.geography = Faker().address()
        self.marital_status = np.random.choice(MARITAL_STATUSES, p=[0.48, 0.36, 0.09, 0.07])
        self.education_level = self.generate_education_level()
        self.employment_status = np.random.choice(EMPLOYMENT_STATUSES, p=[0.65, 0.25, 0.1])
        self.occupation = Faker().job()
        self.citizenship = np.random.choice([True, False], p=[0.95, 0.05])
        self.residential_status = np.random.choice(RESIDENTIAL_STATUS, p=[0.65, 0.35])
        self.parental_status = np.random.choice([True, False], p=[0.69, 0.31])

        self.credit_score = self.generate_credit_score()
        self.month_income = random.randint(6000, 25000)
        self.current_balance = self.generate_current_balance()
        self.total_current_debt = []
        self.total_loans_amount = []
        self.loans_repayment = 0
        self.savings = self.money_amount_with_prob(2000, 4000, [0.7, 0.3])
        self.investment = self.money_amount_with_prob(5000, 10000, [0.3, 0.7])
        self.monthly_expenses = 0
        self.payment_history = 0
        self.num_current_loans = 0
        self.loans_month_payment = []
        self.borrowing_capacity = 0

        self.atm_withdrawals = self.generate_atm_withdrawals()
        self.atm_deposits = self.generate_atm_deposits()
        self.current_balance = self.generate_current_balance()
        self.calls_to_branch = np.random.choice([0, 1, 2], p=[0.85, 0.1, 0.05])
        self.visits_to_branch = np.random.choice([0, 1], p=[0.85, 0.15])
        self.mobile_entrances = np.random.choice(np.arange(0, 5))
        self.online_entrances = np.random.choice(np.arange(0, 1))
        self.calls_to_support = np.random.choice([0, 1], p=[0.85, 0.15])
        self.adds_use = np.random.choice([0, 1], p=[0.95, 0.05])
        self.time_spent = self.generate_time_spent()
        self.customer_feedback = random.randint(0, 5)

    def money_amount_with_prob(self, min_num: int, max_num: int, prob_list: list) -> int:
        """
        Generate a random amount of money with a specified probability of being zero.

        :param
            min_num (int): The minimum amount of money that can be generated.
            max_num (int): The maximum amount of money that can be generated.
            prob_list (list): A list of two probabilities, representing the probabilities of generating
                              zero and generating a number in the range [min_num, max_num], respectively.
                              The two probabilities must sum to 1.

        :return:
            int: A randomly generated amount of money, which is either zero or a number in the range
                 [min_num, max_num], based on the probabilities specified in prob_list.

        :raises:
            ValueError: If the probabilities in prob_list do not sum to 1.
        """
        if sum(prob_list) != 1:
            raise ValueError("Probabilities in prob_list must sum to 1")
        if np.random.choice([True, False], p=prob_list):
            return random.randint(min_num, max_num)
        else:
            return 0

    def generate_date_of_birth(self):
        """
        Generate a birthdate for a client, within a range that would make them eligible for a loan.
        The age range is from 18 to 65, but since we are generating clients two years ago, the age range is
        shifted to 20 to 67.

        :return: A string representing the birthdate.
        """
        return Faker().date_of_birth(minimum_age=20, maximum_age=67)

    def calculate_age(self, timestamp):
        """
        Function to calculate age based on date of birth and timestamp.

        :param timestamp (datetime.datetime): Timestamp to calculate age from.
        :return: int: Age of the client in years.
        """
        return timestamp.year - self.date_of_birth.year - (
                (timestamp.month, timestamp.day) < (self.date_of_birth.month, self.date_of_birth.day))

    def generate_education_level(self) -> str:
        """
        Function to generate education level based on age.
        We know approximately at what age a person can have what maximum degree.

        :return: str: The education level of the person based on their age
        """
        if self.age < 19:
            return EDUCATION_LEVELS[0]
        elif self.age < 22:
            return random.choice(EDUCATION_LEVELS[:2])
        elif self.age < 26:
            return random.choice(EDUCATION_LEVELS[:3])
        else:
            return random.choice(EDUCATION_LEVELS)

    def generate_current_balance(self) -> int:
        """
        Generate current balance and if it is salary day then add month income to current balance.
        :return: int, the client's current balance
        """
        current_balance = random.randint(100, 3000)
        if PAST_DATE.day == 1:
            current_balance += self.month_income
        return current_balance

    def generate_credit_score(self) -> int:
        """
        Generate a credit score in a range of 580-800. This range represents fair, good, and very good scores.
        :return: int, the client's credit score
        """
        return random.randint(580, 800)

    def generate_atm_withdrawals(self) -> int:
        """
        Function generates an amount of money that the client withdrew from an ATM, based on a probability distribution.

        The function first calls the 'money_amount_with_prob' function to generate a random amount of money from a range of 50 to 300,
        with a 20% probability of returning 0, and 80% probability of returning a number in the range.

        If the generated amount is greater than the client's current balance, the function sets the amount to 0 to indicate that
        the withdrawal was unsuccessful.

        The function then subtracts the withdrawal amount from the client's current balance and returns the amount of money
        that was successfully withdrawn from the ATM.
        
        :return int: an amount of money that the client withdrew from an ATM
        """
        atm_withdrawals = self.money_amount_with_prob(50, 300, [0.2, 0.8])
        if atm_withdrawals > self.current_balance:
            atm_withdrawals = 0
        self.current_balance -= atm_withdrawals
        return atm_withdrawals

    def generate_atm_deposits(self) -> int:
        """
        Function generates a random amount for ATM deposits with a given probability and adds it to the current balance.
        :return int: an amount of money for ATM client's deposits
        """
        atm_deposits = self.money_amount_with_prob(50, 300, [0.2, 0.8])
        if atm_deposits > self.current_balance:
            atm_deposits = 0
        self.current_balance += atm_deposits
        return atm_deposits

    def generate_time_spent(self):
        """
        Generates a random amount of time spent by the customer on mobile or online banking platforms. If the customer
        did not use either of these platforms, returns None.
        """
        if self.mobile_entrances != 0 or self.online_entrances != 0:
            return random.randint(2, 10)

    def create_ds_row(self):
        """
        Creates a dictionary representing a row in the dataset, with customer attributes and transaction data.
        """
        return {
            'timestamp': self.timestamp,
            'customer_id': self.customer_id,

            'age': self.age,
            'gender': self.gender,
            'geography': self.geography,
            'marital_status': self.marital_status,
            'education_level': self.education_level,
            'employment_status': self.employment_status,
            'occupation': self.occupation,
            'citizenship': self.citizenship,
            'residential_status': self.residential_status,
            'parental_status': self.parental_status,

            'current_balance': round(self.current_balance, 2),
            'total_current_debt': round(sum(self.total_current_debt), 2),
            'credit_score': self.credit_score,
            'total_loans_amount': round(sum(self.total_loans_amount), 2),
            'loans_repayment': round(self.loans_repayment, 2),
            'savings': round(self.savings, 2),
            'investment': round(self.investment, 2),
            'month_income': round(self.month_income, 2),
            'monthly_expenses': round(self.monthly_expenses * self.month_income, 2),
            'payment_history': self.payment_history,

            'calls_to_branch': self.calls_to_branch,
            'visits_to_branch': self.visits_to_branch,
            'mobile_entrances': self.mobile_entrances,
            'online_entrances': self.online_entrances,
            'atm_withdrawals': self.atm_withdrawals,
            'atm_deposits': self.atm_deposits,
            'calls_to_support': self.calls_to_support,
            'adds_use': self.adds_use,
            'time_spent': self.time_spent,
            'customer_feedback': self.customer_feedback
        }
