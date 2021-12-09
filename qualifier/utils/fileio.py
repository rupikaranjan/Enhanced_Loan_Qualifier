# -*- coding: utf-8 -*-
"""Helper functions to load and save CSV data.

This contains a helper function for loading and saving CSV files.

"""
import csv


def load_csv(csvpath):
    """Reads the CSV file from path provided.

    Args:
        csvpath (Path): The csv file path.

    Returns:
        A header list
        A list of lists that contains the rows of data from the CSV file.

    """
    with open(csvpath, "r") as csvfile:
        data = []
        csvreader = csv.reader(csvfile, delimiter=",")

        # Skip the CSV Header
        header = next(csvreader)

        # Read the CSV data
        for row in csvreader:
            data.append(row)
    return header, data

def save_csv(csvpath, csv_data, csv_header):
    """Saves the csv_header and csv_data into csvpath file.

    Args:
        csvpath (Path): The csv file path to save result data.
        csv_data (List of list): Data to be stored in csv file.
        csv_header: Header for output csv file.

    """

    with open(csvpath, 'w', newline='') as csv_outputfile:
        csv_writer = csv.writer(csv_outputfile)
        csv_writer.writerow(csv_header)
        for bank_data in csv_data:
            csv_writer.writerow(bank_data)
