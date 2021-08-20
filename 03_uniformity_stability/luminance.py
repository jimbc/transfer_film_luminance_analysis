import surface2D as surface
import stat_tools
import pandas as pd
import numpy as np
import data_handling as dh

class Luminance:
    def __init__(self, src_path):
        self.df = self.read(src_path)

    @classmethod
    def read(cls, file_patch):
        data = dh.read_atlas(file_patch)
        return data

    def calc_stats(self):
        metrics = pd.DataFrame()
        list_columns = self.data.columns
        for col in list_columns[1:]:
            metrics.loc['mean', col] = self.data[col].mean(axis=0)
            metrics.loc['std', col] = self.data[col].std(axis=0)
            metrics.loc['var', col] = self.data[col].var(axis=0)
            metrics.loc['count', col] = self.data[col].count()
            data = [el for el in self.data[col] if not np.isnan(el)]
            metrics.loc['conf', col] = stat_tools.confidence_value(data, confidence=0.95)
        return metrics

    def to_excel(self, dst_path):
        writer = pd.ExcelWriter(dst_path, engine='xlsxwriter')
        self.data.to_excel(writer, sheet_name='data')
        self.stats.to_excel(writer, sheet_name='stats')
        writer.save()


class LumStability(Luminance):
    def __init__(self, src_path):
        super().__init__(src_path)
        self.data = self.eval()
        self.stats = self.calc_stats()
        self.keys = list(self.__dict__.keys())
        self.values = list(self.__dict__.values())
        self.items = list(self.__dict__.items())

    def eval(self):
        self.df.data.sort_values(['wear_track_lateral_position', 'segment_elapsed_time'])
        list_track_position = self.df.data['wear_track_lateral_position'].unique()
        list_track_position.sort()

        result_matrix = pd.DataFrame({'wear_track_lateral_position': list_track_position})
        result_matrix = result_matrix.apply(self.calc_metrics, data=self.df.data, axis=1)

        return result_matrix

    @staticmethod
    def calc_metrics(position, data):
        data_filter = data['wear_track_lateral_position'] == float(position)
        primary = data[data_filter].reset_index(drop=True)

        sample_width = data['segment_elapsed_time'].max()
        primary = primary['delta_l_rel'].to_list()
        res = surface.Surface(primary, cutoff=sample_width / 7, sample_width=sample_width)
        position['La_roi'] = res.metrics['Ra']
        position['Lz_roi'] = res.metrics['Rz']
        position['Sa_roi'] = 1 / res.metrics['Ra']
        position['Sz_roi'] = 1 / res.metrics['Rz']
        return position


class LumUniformity(Luminance):
    def __init__(self, src_path):
        super().__init__(src_path)
        self.data = self.eval()
        self.stats = self.calc_stats()

    def eval(self):
        self.df.data.sort_values(['segment_elapsed_time', 'wear_track_lateral_position'])
        list_track_position = self.df.data['segment_elapsed_time'].unique()
        list_track_position.sort()

        result_matrix = pd.DataFrame({'segment_elapsed_time': list_track_position})
        result_matrix = result_matrix.apply(self.calc_metrics, data=self.df.data, axis=1)
        return result_matrix

    @staticmethod
    def calculate_amplitude(arr):
        arr_min = min(arr)
        arr_max = max(arr)
        if (arr_min < 0 and arr_max < 0) or (arr_min > 0 and arr_max > 0):
            return max(arr) - min(arr)
        else:
            return max(arr) + np.abs(min(arr))

    @staticmethod
    def calc_rz(data_arr):
        segment_length = len(data_arr) // 5
        first = 0
        last = segment_length
        data_corr = data_arr / (sum(data_arr) / len(data_arr)) - 1

        res = []
        for i in range(5):
            temp = data_corr[first:last]
            res.append(LumUniformity.calculate_amplitude(temp))
            first += segment_length
            last += segment_length

        return {'Rz': sum(res) / len(res),
                'Rz1max': max(res)
                }

    @classmethod
    def calc_metrics(cls, position, data):
        data_filter = data['segment_elapsed_time'] == float(position)
        primary = data[data_filter].reset_index(drop=True)

        primary = primary['delta_l_rel'].to_numpy()
        metric_rz = LumUniformity.calc_rz(primary)
        position['Uz_roi'] = 1 / metric_rz['Rz']

        return position


if __name__ == '__main__':
    from datetime import datetime
    file_path = '00547783.0001.xt'
    time_start = datetime.now()

    test_stability = LumStability(file_path)
    test_stability.to_excel('stability.xlsx')

    test_uniformity = LumUniformity(file_path)
    test_uniformity.to_excel('uniformity.xlsx')
    print('eval finished in', datetime.now() - time_start)
