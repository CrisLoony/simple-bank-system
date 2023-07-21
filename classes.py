from abc import ABC, abstractmethod
from datetime import date
from time import sleep

from func import calc_interest, calculateAge, generate_acc_number


class Customer:
    def __init__(self, name: str, birthYear: int, birthMonth: int, birthDay: int, location: str, income: int):
        self.name = name
        self.birthYear = birthYear
        self.birthMonth = birthMonth
        self.birthDay = birthDay
        self.income = income
        self.location = location

        self.birthDate = date(self.birthYear, self.birthMonth, self.birthDay)
        self.age = calculateAge(self.birthDate)

        self.account = None
        self.accountNumber = None


class Bank:
    def __init__(self, bankName: str, bankLocation: str) -> None:

        self.bankName = bankName
        self.bankLocation = bankLocation

        self._customers = []
        self._acc_numbers_savings = []
        self._acc_numbers_checking = []
        self.account_types = ['Savings Account', 'Checking Account']

    def create_account(self, customer: Customer, accountType: str):
        if customer.age >= 18:
            self._customers.append(customer.name)

            print(f"Wait while we create your account number.")
            sleep(1)

            while True:
                account_number = generate_acc_number(9)

                if account_number not in self._acc_numbers_savings or self._acc_numbers_checking:
                    if accountType == self.account_types[0]:
                        self._acc_numbers_savings.append(account_number)
                        customer.accountNumber = account_number
                        customer.account = "Savings Account"
                        print(
                            f"Your account number is: \033[33m{account_number}\033[m.", end=' ')
                        print(
                            f"Your acccount type is: '{self.account_types[0]}'.")
                        sleep(1)
                        print(f"You were successfully registered. \n")
                        break

                    elif accountType == self.account_types[1]:
                        self._acc_numbers_checking.append(account_number)
                        customer.accountNumber = account_number
                        customer.account = "Checking Account"
                        print(
                            f"Your account number is: \033[33m{account_number}\033[m. \n")
                        print(
                            f"Your acccount type is: '{self.account_types[1]}.'")
                        sleep(1)
                        print(f"You were successfully registered. \n")
                        break

                    else:
                        print(
                            f"Our bank don't works with the type of account: '{accountType}'.")
                        print(f"Create a Savings or Checking Account.")
                        return False

                else:
                    continue
            return True

        print(f"You aren't old enough to create an account. \n")
        return False

    def authenticate_customer_savings(self, customer: Customer):
        if customer.name in self._customers and customer.accountNumber in self._acc_numbers_savings:
            return True
        return False

    def authenticate_customer_checking(self, customer: Customer):
        if customer.name in self._customers and customer.accountNumber in self._acc_numbers_checking:
            return True
        return False


class Account(ABC):
    def __init__(self, customer: Customer, bank: Bank) -> None:
        super().__init__()
        self.customer = customer
        self.bank = bank
        self.balance = 0

    def deposit(self, amount: int):
        condition = self.bank.authenticate_customer_savings(
            self.customer) or self.bank.authenticate_customer_checking(self.customer)
        if condition:
            self.balance += amount
            print(f'The value ${amount:.2f} was deposited successfully.')
            print(f"Your balance is: ${self.balance:.2f}")

        else:
            print(
                f"The customer {self.customer.name} don't have an account with us, try with another bank.")

    @abstractmethod
    def withdraw(self, amount: int):
        pass


class SavingsAccount(Account):
    def withdraw(self, amount: int):
        print(f'You want to withdraw ${amount:.2f}.')
        if self.bank.authenticate_customer_savings(self.customer):
            if self.balance >= amount:
                self.balance -= amount
                print(f"You withdrew ${amount:.2f}")
                print(f"Your balance is: ${self.balance:.2f}.")
            else:
                print(f"Insufficient funds.")
        else:
            print('Withdraw not authorized.')


class CheckingAccount(Account):
    def __init__(self, customer: Customer, bank: Bank) -> None:
        super().__init__(customer, bank)
        self.credit = 0

    def verify_credit_approvement(self):
        if self.customer.income > 3000 and self.customer.location == self.bank.bankLocation:
            self.credit = 1000
            return True

        elif self.customer.income > 7000:
            self.credit = 2000
            return True

        else:
            return False

    def withdraw(self, amount: int, useCredit: bool = False):
        credit_cont = 0
        while True:
            print(f'You want to withdraw ${amount:.2f}.')
            if self.bank.authenticate_customer_checking(self.customer):
                if self.balance >= amount:
                    self.balance -= amount
                    print(f"You withdrew ${amount:.2f}")
                    print(f"Your balance is: ${self.balance:.2f}.")
                    break

                elif credit_cont == 1:
                    print(
                        '\nInsufficient funds and you already used your credit limit.\n')
                    break

                elif self.balance < amount and self.verify_credit_approvement() and useCredit:
                    print(
                        f"Your balance is under the amount that you want to withdraw.")
                    print(f"We're going to use your credit limit. \n ...")
                    self.balance += self.credit
                    credit_cont += 1
                    print(f'Your balance is: ${self.balance:.2f}.')
                    print(f"Please wait while we carry out your withdrawal.")
                    continue

                else:
                    print('Insufficient funds.')
            else:
                print('Withdraw not authorized.')


class Loan(ABC):
    def __init__(self, customer: Customer, bank: Bank) -> None:
        self.customer = customer
        self.bank = bank

    @abstractmethod
    def verify_approvement(self):
        pass


class PersonalLoan(Loan):
    def __init__(self, customer: Customer, bank: Bank) -> None:
        super().__init__(customer, bank)
        self.interestRate = 4

    def verify_approvement(self):
        if self.customer.income > 1000:
            return True
        return False

    def personal_loan(self, account: Account, amount: int, installments: int):
        bank_autenticate_customer = self.bank.authenticate_customer_savings(
            self.customer) or self.bank.authenticate_customer_savings(self.customer)
        if self.verify_approvement() and bank_autenticate_customer:
            installment_value = int(calc_interest(
                self.interestRate, amount) / installments)
            print(f'Your Loan was approved.')
            account.balance += amount
            sleep(0.5)
            print(f"You're taking a Personal Loan of ${amount:.2f}", end=' ')
            print(f"with an interest rate of {self.interestRate}%", end=' ')
            print(
                f"to pay in {installments} installments in the amount of ${installment_value:.2f} ", end=' ')
            print('per month.')
            print(f"The value of ${amount:.2f} is already in your account.")

        else:
            print("The loan wan't authorized.")


class CollateralizedLoan(Loan):
    def __init__(self, customer: Customer, bank: Bank) -> None:
        super().__init__(customer, bank)
        self.interestRate = 3
        self.condition_income_less3000 = self.customer.income <= 3000
        self.condition_income_less5000 = 3000 < self.customer.income < 5000
        self.condition_income_more5000 = self.customer.income >= 5000
        self.condition_age30 = self.customer.age < 30
        self.condition_location = self.customer.location == self.bank.bankLocation

    def verify_approvement(self):
        if self.condition_income_less3000 and self.condition_age30 and self.condition_location:
            return True

        elif self.condition_income_less5000 and self.condition_location:
            return True

        elif self.condition_income_more5000 and self.condition_age30:
            return True
        else:
            return False

    def collateralized_loan(self, account: SavingsAccount or CheckingAccount, amount: int, installments: int):
        bank_authenticate_customer = self.bank.authenticate_customer_savings(
            self.customer) or self.bank.authenticate_customer_checking(self.customer)
        if self.verify_approvement() and bank_authenticate_customer:
            installment_value = int(calc_interest(
                self.interestRate, amount) / installments)
            print(f'Your Loan was approved.')
            account.balance += amount
            print(f"The value of ${amount:.2f} is already in your account.")
            sleep(0.5)
            print(f"You're taking a Personal Loan of ${amount:.2f}", end=' ')
            print(f"with an interest rate of {self.interestRate}%", end=' ')
            print(
                f"to pay in {installments} installments in the amount of ${installment_value:.2f}.", end=' ')
            print('per month.')

        else:
            print("The loan wasn't authorized.")


class PayrollLoan(Loan):
    def __init__(self, customer: Customer, bank: Bank) -> None:
        super().__init__(customer, bank)
        self.interestRate = 2
        self.condition_income_more5000 = self.customer.income >= 5000
        self.condition_age30 = self.customer.age < 30

    def verify_approvement(self):
        if self.condition_income_more5000 and self.condition_age30:
            return True
        return False

    def payroll_loan(self, account: SavingsAccount or CheckingAccount, amount: int, installments: int):
        bank_authenticate_customer = self.bank.authenticate_customer_savings(
            self.customer) or self.bank.authenticate_customer_checking(self.customer)
        if self.verify_approvement() and bank_authenticate_customer:
            installment_value = int(calc_interest(
                self.interestRate, amount) / installments)
            print(f'Your Loan was approved.')
            account.balance += amount
            print(f"The value of ${amount:.2f} is already in your account.")
            sleep(0.5)
            print(f"You're taking a Personal Loan of ${amount:.2f}", end=' ')
            print(f"with an interest rate of {self.interestRate}%", end=' ')
            print(
                f"to pay in {installments} installments in the amount of ${installment_value:.2f}.", end=' ')
            print('per month.')

        else:
            print("The loan wasn't authorized.")
