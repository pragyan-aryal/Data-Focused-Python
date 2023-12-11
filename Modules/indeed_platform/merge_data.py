import pandas as pd


def merge_data(codes, sample="All"):
    frame = []

    for code in codes:
        try:
            frame.append(pd.read_csv('Final_Data/' + sample + "/" + code + '_final.tsv', sep='\t'))
        except:
            pass

    df = pd.concat(frame, ignore_index=True)

    df = df.drop_duplicates('Key')

    df.to_parquet('Final_Data/' + sample + '/merged.parquet', index=False)

