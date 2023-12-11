import pandas as pd
import re


def clean_salary(sample="All"):
    print('\n Currently cleaning the salary info for each job')

    df = pd.read_parquet('Final_Data/' + sample + '/merged.parquet')

    pattern = r'\$([\d,]+(?:\.\d+)?)\s*(?:- \$([\d,]+(?:\.\d+)?))?'

    df['MinSalary'] = None
    df['MaxSalary'] = None

    # Iterate over the rows of the 'Salary' column
    for index, row in df.iterrows():
        line = row['Salary']
        if line is not None:
            match = re.search(pattern, str(line))
            if match:
                min_salary, max_salary = match.groups()
                df.at[index, 'MinSalary'] = float(min_salary.replace(',', '')) if min_salary else None
                df.at[index, 'MaxSalary'] = float(max_salary.replace(',', '')) if max_salary else None

    pattern_hour_range = r'\$([\d,]+(?:\.\d+)?)\s*-\s*\$([\d,]+(?:\.\d+)?)\s*an hour'
    pattern_hour_single = r'\$([\d,]+(?:\.\d+)?)\s*an hour'
    for index, row in df.iterrows():
        line = row['Salary']
        if line is not None:
            # Check for hourly rates specified as a range
            match_hourly_range = re.search(pattern_hour_range, str(line))
            if match_hourly_range:
                min_hourly, max_hourly = match_hourly_range.groups()
                min_hourly = float(min_hourly.replace(',', '')) if min_hourly else None
                max_hourly = float(max_hourly.replace(',', '')) if max_hourly else None
                df.at[index, 'MinSalary'] = min_hourly * 1920
                df.at[index, 'MaxSalary'] = max_hourly * 1920 if max_hourly else None
            else:
                # Check for hourly rates specified as a single value
                match_hourly_single = re.search(pattern_hour_single, str(line))
                if match_hourly_single:
                    min_hourly = match_hourly_single.group(1)
                    min_hourly = float(min_hourly.replace(',', '')) if min_hourly else None
                    df.at[index, 'MinSalary'] = min_hourly * 1920

    pattern_month = r'(?:From\s*)?\$([\d,]+(?:\.\d+)?)\s*(?:- \$([\d,]+(?:\.\d+)?))?\s*a\s*month'
    # Separate loop for updating monthly rates
    for index, row in df.iterrows():
        line = row['Salary']
        if line is not None:
            match_monthly = re.search(pattern_month, str(line))
            if match_monthly:
                min_monthly, max_monthly = match_monthly.groups()
                min_monthly = float(min_monthly.replace(',', '')) if min_monthly else None
                max_monthly = float(max_monthly.replace(',', '')) if max_monthly else None
                df.at[index, 'MinSalary'] = min_monthly * 12
                df.at[index, 'MaxSalary'] = max_monthly * 12 if max_monthly else None  # No defined max for monthly rates

    df.to_parquet('Final_Data/' + sample + '/merged.parquet', index=False)
