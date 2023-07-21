from classes import (Bank, CheckingAccount, CollateralizedLoan, Customer,
                     PayrollLoan, PersonalLoan, SavingsAccount)

if __name__ == '__main__':
    kdbBank = Bank('KDB Bank', 'Seoul')
    bb = Bank('Banco do Brasil', 'Brasil')
    jk = Customer('João Carlos', 1997, 7, 1, 'Seoul', 2500)
    print(jk.name)
    kdbBank.create_account(jk, 'Savings Account')

    jk_account = SavingsAccount(jk, kdbBank)
    jk_account.deposit(5000)
    jk_account.withdraw(100)
    jk_account2 = SavingsAccount(jk, bb)
    jk_account2.deposit(3000)
    jk_personal_loan = PersonalLoan(jk, kdbBank)
    jk_personal_loan.personal_loan(jk_account, 60000, 45)

    print('-' * 50)

    nj = Customer('Nikolas Jorge', 1994, 7, 15, 'Seoul', 9000)
    print(nj.name)
    kdbBank.create_account(nj, 'Checking Account')

    nj_account = CheckingAccount(nj, kdbBank)
    nj_account.withdraw(5000, True)
    nj_account.deposit(6000)
    nj_account.withdraw(2000, True)
    nj_collateralized_loan = CollateralizedLoan(nj, kdbBank)
    nj_collateralized_loan.collateralized_loan(nj_account, 152000, 36)

    print('-' * 50)

    cris = Customer('Ana Cristina', 2003, 4, 9, 'Brasil', 2500)
    print(cris.name)
    bb.create_account(cris, 'Savings Account')
    cris_account = SavingsAccount(cris, bb)
    cris_payroll_loan = PayrollLoan(cris, bb)
    cris_payroll_loan.payroll_loan(cris_account, 5000, 10)

    print('-' * 50)

    carlos = Customer('Carlos Henrique', 1996, 8, 2, 'Brasil', 8000)
    print(carlos.name)
    bb.create_account(carlos, 'Savings Account')
    carlos_account = SavingsAccount(carlos, bb)
    carlos_payroll_loan = PayrollLoan(carlos, bb)
    carlos_payroll_loan.payroll_loan(carlos_account, 5000, 30)
    print('-' * 50)

    louyse = Customer('Louyse Maria', 2023, 4, 3, 'Brasil', 0)
    print(louyse.name)
    bb.create_account(louyse, 'Savings Account')

    print('-' * 50)

    laura = Customer('Laura Maria', 2000, 2, 1, 'Brasil', 1500)
    print(laura.name)
    bb.create_account(laura, 'Account')
