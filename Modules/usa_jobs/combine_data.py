import pandas as pd
import os


def combine_data(sample="All"):
    csv_directory = 'Final_Data/' + sample

    # List to store individual DataFrames
    dataframes = []

    # Loop through all CSV files in the directory
    for filename in os.listdir(csv_directory):
        if filename.endswith('.csv'):
            # Read each CSV file into a DataFrame
            file_path = os.path.join(csv_directory, filename)
            df = pd.read_csv(file_path)

            # Append the DataFrame to the list
            dataframes.append(df)

    # Concatenate all DataFrames into one
    combined_df = pd.concat(dataframes, ignore_index=True)

    # Write the combined DataFrame to a new CSV file
    combined_df.to_csv('Final_Data/' + sample + '/USA_JOBS.csv', index=False)
