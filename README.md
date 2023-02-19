### How to run it
- Download __*.zip__ file
- Unzip it at any suitable folder
- Install all libs from __requirements.txt__
- Make sure you pass as CLI argument "-n <i>\<number of clients></i>" (bu default `num_clients=1000`)
- Run __main.py__
- That's all

```bash
pip install -r requirements.txt
python main.py -n num_clients
```

### Structure of files
- __[venv]__ - environment folder
- __requirements.txt__ - file list off all needed modules
- __main__ - primary startup file
- __customer__ - class that generate customer
- __loan__ - class that generate loan

### Assumptions:

> Assuming that all of our clients are existing bank clients, we can gather some historical data before approving loans. To create clients, we will use a date that is two years prior to today's date. However, it is possible that some clients may not meet the requirements to qualify for loans.
> 
> To ensure fairness, it would be wise to distribute loans at different times for clients. To accomplish this, I suggest randomly selecting more clients to receive loans during the first part of the year.
> 
> In order to maintain a level of financial stability, it is important that we do not provide loans to unemployed individuals. Therefore, we will only consider clients who are either full-time, part-time, or self-employed.
> 
> To be eligible for a loan, clients must be between the ages of 18 and 65, assuming they have completed their education. Additionally, I have decided to generate fake geographic locations for each client.
> 
> For consistency, all clients will receive their salaries on the first day of the month, and loan payments will be due on the 15th. Clients will be required to add to their savings on the 17th and investments on the 19th. Benefit returns will be provided on the 25th and 30th, respectively.
> 
> To ensure a unique identifier, I suggest generating a loan ID using a combination of the customer ID, unique ID, and date of the loan. As one customer cannot take out two loans on the same date, the ID will be unique each time.

### Per client per day Dataset Description:
1. `timestamp`: In this particular dataset, there are 365 * 2 snapshots, which means that for each client, there is a record for every day of the last two years.
2. `customer_id`: A unique identifier assigned to each customer.
3. `age`: The age of the client, which can be an indicator of their overall financial stability, their likelihood to need a loan, and their ability to repay a loan.
4. `gender`: The gender of the client, which may be relevant for demographic or marketing purposes, but should not be used to determine loan approval or interest rates. 
5. `geography`: The location of the client, which can be used to determine relevant state or local regulations, as well as any regional economic factors that may affect their financial situation. (Fake data in our dataset, randomly generated.)
6. `marital_status`: The marital status of the client, including whether they are single, married, divorced, or widowed. This can provide insight into the client's overall financial stability, as well as any joint financial obligations they may have with a spouse. 
7. `education_level`: The highest level of education completed by the client, which can be an indicator of their earning potential and financial stability.
8. `employment_status`: The client's current employment status, including whether they are employed full-time, part-time, self-employed.
9. `occupation`: Job title refers to the specific type of work or profession that the client is engaged in. This feature can provide information on the client's income level, stability of employment, and potential for future income growth.
10. `citizenship`: the person's country of citizenship or immigration status, such as citizen - True or non-citizen - False.
11. `residential_status`: whether the client owns or rents their home.
12. `parental_status`: The client's parental status can provide insight into their financial obligations and potential ability to repay a loan.
13. `current_balance`: The current balance in the client's bank account, which can provide insight into their overall financial stability and ability to repay a loan.
14. `current_debt`: The current amount of debt owed by the client, including outstanding loans. This can provide insight into the client's overall financial situation and their ability to repay a loan.
15. `credit_score`: A numerical score that represents the client's creditworthiness, based on their credit history and other financial factors. This can be used to determine loan approval and interest rates.
16. `loan_amount`: The amount of the loan being requested by the client, which can be used to determine loan approval and interest rates.
17. `loan_repayment`: The amount of money that client paid on all loans that have on the current date.
18. `savings`: The amount of money the client has saved, which can be used to determine their overall financial stability and ability to repay a loan. 
19. `investment`: The client's investment portfolio, including any stocks, bonds, or other assets they hold. This can be used to determine their overall financial stability and risk tolerance.
20. `month_income`: The client's monthly income, which can be used to determine their ability to repay a loan.
21. `monthly_expenses`: The client's monthly expenses, including rent, utilities, and other bills, which can be used to determine their ability to repay a loan.
22. `payment_history`: The client's history of making payments on previous loans not on time, which can be used to determine their creditworthiness and ability to repay a loan.
23. `calls_to_branch`: The number of phone calls that the client has made to the bank's branch offices, which can provide insight into their level of engagement with the bank and the customer service they have received. 
24. `visits_to_branch`: The number of in-person visits that the client has made to the bank's branch offices, which can provide similar insights as calls to branch.
25. `mobile_entrances`: The number of times that the client has accessed the bank's mobile app, which can provide insight into their preference for digital banking and their level of engagement with the bank's digital services. 
26. `online_entrances`: The number of times that the client has accessed the bank's online banking platform, which can provide similar insights as mobile entrances. 
27. `atm_withdrawals`: The number of times that the client has withdrawn money from the bank's ATMs, which can provide insight into their overall banking habits and financial needs. 
28. `atm_deposits`: The number of times that the client has made deposits at the bank's ATMs, which can provide similar insights as ATM withdrawals. 
29. `calls_to_support`: The number of phone calls that the client has made to the bank's customer support or help desk, which can provide insight into their level of satisfaction with the bank's services and their need for assistance. 
30. `ads_use`: The level of engagement with the bank's advertising materials or promotions, which can provide insight into the client's level of interest in the bank's services and their potential willingness to take out a loan.
31. `time_spent` on mobile/online banking: The average amount of time that the client spends using the bank's mobile or online banking services, which can provide insight into their level of engagement and potential interest in other bank products. 
32. `customer_feedback`: The client's rating or feedback on the bank's services, which can provide insight into their level of satisfaction and their potential willingness to take out a loan.

### Loan Dataset Description:
1. `loan_id`: A unique identifier assigned to each loan issued by the bank.
2. `customer_id`: A unique identifier assigned to each customer who has taken out a loan.
3. `date`: The date on which the loan was issued.
4. `loan_size`: The total amount of money that was borrowed by the customer.
5. `loan_type`: The type of loan that was issued.

### Statistical Information

According to the Central Bureau of Statistics in Israel, as of 2021, the homeownership rate in Israel is approximately 68.2%, which means that a majority of households (about two-thirds) in Israel own their homes. The remaining households are renters.

According to data from the Central Bureau of Statistics in Israel, as of 2021, the marital status of the Israeli population aged 15 and over is as follows:
- 47.6% of the population is married
- 35.8% of the population has never been married
- 9.2% of the population is divorced
- 7.4% of the population is widowed

According to data from the Central Bureau of Statistics in Israel, as of 2021, the gender distribution of the Israeli population is as follows:
- 50.5% of the population is male
- 49.5% of the population is female 

According to data from the Central Bureau of Statistics in Israel, as of 2021, the parental status of the Israeli population aged 20-44 is as follows:
* 63.8% of women and 72.1% of men have children
* 35.1% of women and 26.3% of men do not have children
* 1.1% of women and 1.6% of men did not report their parental status