import pandas as pd


def merge_job(codes, sample="All"):
    for code in codes:
        output_file_name = code + '.tsv'

        columns = ['Key', 'Company', 'Position', 'Location', 'Category', 'Experience_Level', 'Salary']

        frame = []

        try:
            entry_level = pd.read_csv('Final_Data/' + sample + "/" + code + '_ENTRY_LEVEL.tsv', sep='\t')
            re_1 = entry_level.columns
            entry_level.columns = columns
            entry_level.loc[-1] = re_1
            entry_level.index = entry_level.index + 1
            entry_level.sort_index(inplace=True)

            frame.append(entry_level)
        except:
            pass

        try:
            mid_level = pd.read_csv('Final_Data/' + sample + "/" + code + '_MID_LEVEL.tsv', sep='\t')
            rm_1 = mid_level.columns
            mid_level.columns = columns
            mid_level.loc[-1] = rm_1
            mid_level.index = mid_level.index + 1
            mid_level.sort_index(inplace=True)

            frame.append(mid_level)
        except:
            pass

        try:
            senior_level = pd.read_csv('Final_Data/' + sample + "/" + code + '_SENIOR_LEVEL.tsv', sep='\t')
            rs_1 = senior_level.columns
            senior_level.columns = columns
            senior_level.loc[-1] = rs_1
            senior_level.index = senior_level.index + 1
            senior_level.sort_index(inplace=True)

            frame.append(senior_level)
        except:
            pass

        df = pd.concat(frame, ignore_index=True)

        df = df.drop_duplicates('Key')

        if sample == "All":
            df.to_csv('Final_Data/All/' + output_file_name, sep='\t', index=False)
        else:
            df.to_csv('Final_Data/Sample/' + output_file_name, sep='\t', index=False)
