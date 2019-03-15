# BackbaseAssignment
Solution to problem provided by Backbase using Python 3.6.2

to use programme type in: <br />
Backbase.py  [input csv file]

Backbase.py file takes in an input csv file containing transacations of a Customer's Current and Savings Account of the format:
AccountId, AccountType, InitiatorType, DateTime, Transaction Value

And returns an output csv file called "result.cvs" with the same format but with added Transactions with InitiatorType of "SYSTEM".
Where the transactions are Withdrawals from the Savings Account and Deposits to the Current Account.
The "SYSTEM" Transactions will happen if the Current Account encounters a Withdrawal transaction that will cause it to fall below
£0. It then takes the necessary amount from the Savings Account- depending on if the Account Balance is over £0.
In the case where all the money in the Savings account has been depleted, the Current account balance is put into overdraft.

If there are multiple Savings Accounts, the first Savings account mentioned in the input csv file will be withdrawn from first.
In the case where the withdrawal amount was too much for the first savings account, the first savings account will transfer all
its balance to the Current account and move on to the next savings account. This continues until the Current Account will no longer
reach below £0 or if all the Savings accounts have been depleted.
