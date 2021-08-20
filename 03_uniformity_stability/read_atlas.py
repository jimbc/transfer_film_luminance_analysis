import pandas as pd
import os
import yaml


class AtlasData():

    def __init__(self, path):
        self.header = self.read_header(path)
        self.data = self.read_values(path, self.header.columns)

    @staticmethod
    def read_values(path, header):
        data = pd.read_csv(path, sep='\t', skiprows=1, names=header)
        return data

    @staticmethod
    def read_header(file_path):
        folder_path, fn = os.path.split(file_path)
        fn_split = fn.split('.')

        if fn_split[-1] == 'xt':
            fn = f"{fn_split[0]}.{fn_split[1]}.{fn_split[2]}.header.yaml"
        else:
            fn = f"{fn_split[0]}.{fn_split[2]}.header.yaml"

        if folder_path:
            file_path = f'{folder_path}/{fn}'
        else:
            file_path = fn

        with open(f'{file_path}', 'r') as f:
            res = yaml.load(f, Loader=yaml.Loader)

        res = res.get(':column_descriptor', res)  # gives content of column descriptor if exists, else no change
        df = pd.DataFrame(res)
        df = df.rename(columns=lambda x: x.strip(':'), index=lambda x: x.strip(':'))
        df = df.sort_values(['index'], axis=1)
        return df


if __name__ == '__main__':
    import datetime
    time_start = datetime.datetime.now()
    test_file_path_xt = r'C:\Users\jim\Documents\Python_projects\jbc_tools\data\set_1619\00549374.0001.xt'
    test_xt = AtlasData(test_file_path_xt)

    test_file_path_proc = r'C:\Users\jim\Documents\Python_projects\jbc_tools\data\set_1619\00549374.0001.proc'
    test_proc = AtlasData(test_file_path_proc)
    print(f'finished in {datetime.datetime.now()-time_start}')
