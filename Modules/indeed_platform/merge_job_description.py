import pandas as pd


def merge_data_description(codes, sample="All"):
    print('\nCurrently merging the job details and description')

    for code in codes:
        data_1 = 'Final_Data/' + sample + '/' + code + '.tsv'
        data_2 = 'Final_Data/' + sample + '/' + code + '_desc.tsv'

        df1 = pd.read_csv(data_1, sep='\t')
        df2 = pd.read_csv(data_2, sep='\t')

        columns = ['Key', 'Description', 'Benefits']

        re_1 = df2.columns
        df2.columns = columns
        df2.loc[-1] = re_1
        df2.index = df2.index + 1
        df2.sort_index(inplace=True)

        merged = pd.merge(df1, df2, on='Key', how='inner')

        merged = merged.drop_duplicates('Key')

        merged.to_csv('Final_Data/' + sample + '/' + code + '_final.tsv', sep='\t', index=False)
