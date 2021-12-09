# -*- coding: utf-8 -*-
"""Loan Qualifier Application.

This is a command line application to match applicants with qualifying loans.

Example:
    $ python app.py
"""
import sys
import fire
import questionary
from pathlib import Path
from qualifier.utils.fileio import load_csv, save_csv

from qualifier.utils.calculators import (
    calculate_monthly_debt_ratio,
    calculate_loan_to_value_ratio,
)

from qualifier.filters.max_loan_size import filter_max_loan_size
from qualifier.filters.credit_score import filter_credit_score
from qualifier.filters.debt_to_income import filter_debt_to_income
from qualifier.filters.loan_to_value import filter_loan_to_value


def load_bank_data():
    """Ask for the file path to the latest banking data and load the CSV file.

    Returns:
        The bank data and header list from the data rate sheet CSV file.
    """

    csvpath = questionary.text("Enter a file path to a rate-sheet (.csv):").ask()
    csvpath = Path(csvpath)
    if not csvpath.exists():
        sys.exit(f"Oops! Can't find this path: {csvpath}")

    return load_csv(csvpath)


def get_applicant_info():
    """Prompt dialog to get the applicant's financial information.

    Returns:
        Returns the applicant's financial information.
    """

    credit_score = questionary.text("What's your credit score?").ask()
    debt = questionary.text("What's your current amount of monthly debt?").ask()
    income = questionary.text("What's your total monthly income?").ask()
    loan_amount = questionary.text("What's your desired loan amount?").ask()
    home_value = questionary.text("What's your home value?").ask()

    credit_score = int(credit_score)
    debt = float(debt)
    income = float(income)
    loan_amount = float(loan_amount)
    home_value = float(home_value)

    return credit_score, debt, income, loan_amount, home_value


def find_qualifying_loans(bank_data, credit_score, debt, income, loan, home_value):
    """Determine which loans the user qualifies for.

    Loan qualification criteria is based on:
        - Credit Score
        - Loan Size
        - Debit to Income ratio (calculated)
        - Loan to Value ratio (calculated)

    Args:
        bank_data (list): A list of bank data.
        credit_score (int): The applicant's current credit score.
        debt (float): The applicant's total monthly debt payments.
        income (float): The applicant's total monthly income.
        loan (float): The total loan amount applied for.
        home_value (float): The estimated home value.

    Returns:
        A list of the banks willing to underwrite the loan.

    """

    # Calculate the monthly debt ratio
    monthly_debt_ratio = calculate_monthly_debt_ratio(debt, income)
    print(f"\nThe monthly debt to income ratio is {monthly_debt_ratio:.02f}")

    # Calculate loan to value ratio
    loan_to_value_ratio = calculate_loan_to_value_ratio(loan, home_value)
    print(f"The loan to value ratio is {loan_to_value_ratio:.02f}.")

    # Run qualification filters
    bank_data_filtered = filter_max_loan_size(loan, bank_data)
    bank_data_filtered = filter_credit_score(credit_score, bank_data_filtered)
    bank_data_filtered = filter_debt_to_income(monthly_debt_ratio, bank_data_filtered)
    bank_data_filtered = filter_loan_to_value(loan_to_value_ratio, bank_data_filtered)

    print(f"\nFound {len(bank_data_filtered)} qualifying loans")

    return bank_data_filtered

def save_qualifying_loans(qualifying_loans, header):
    """Promts user whether to save the qualifying loans to a CSV file.
     and promts them for output file path if they wish to save the details.

    Args:
        qualifying_loans (list of lists): The qualifying bank loans.
        header (list): Header list for the output csv file
    """

    # Asking user whether the user wish to save the qualifying loan details.
    save_to_csv = questionary.text("Do you want to save your qualifying loan details in a csv file? (y/n) : ").ask()
    
    if save_to_csv == "y":

        # Not saving if there are no qualifying loans.
        if len(qualifying_loans) == 0:
            sys.exit(f"\nSorry! Since there are no qualifying loans it cannot be saved.")
        else:

            #Promping user for output filepath
            output_filepath = questionary.text("Please Enter the csv file path : ").ask()

            #Checking if the entered filepth is a .csv file
            if ".csv" not in output_filepath:
                output_filepath = output_filepath + ".csv"

            #Saving the qualified loan details in the user specified output file.
            csvpath = Path(output_filepath)
            save_csv(csvpath, qualifying_loans, header)
            print(f"\nThe Qualified Loan data list is stored in ", output_filepath)
    else:
        sys.exit(f"\nThank you! The qualified loan details are not saved in a file!")

def run():
    """The main function for running the script."""

    # Load the latest Bank data
    bank_data_header, bank_data = load_bank_data()

    # Get the applicant's information
    credit_score, debt, income, loan_amount, home_value = get_applicant_info()

    # Find qualifying loans
    qualifying_loans = find_qualifying_loans(
        bank_data, credit_score, debt, income, loan_amount, home_value
    )

    # Save qualifying loans
    save_qualifying_loans(qualifying_loans, bank_data_header)


if __name__ == "__main__":
    fire.Fire(run)
