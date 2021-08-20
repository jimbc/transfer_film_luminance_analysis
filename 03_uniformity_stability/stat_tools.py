import scipy.stats as stats
import numpy as np


def pearson_corr(array1, array2):
    pearson_corr, _ = stats.pearsonr(array1, array2)
    return pearson_corr


def spearman_corr(array1, array2):
    spearman_corr, _ = stats.spearmanr(array1, array2)
    return spearman_corr


def mean_confidence_interval(data, confidence=0.95):
    a = 1.0 * np.array(data)
    n = len(a)
    m, se = np.mean(a), stats.sem(a)

    h = se * stats.t.ppf((1 + confidence) / 2., n - 1)
    return m, m - h, m + h


def confidence_value(data, confidence=0.95):
    a = 1.0 * np.array(data)
    n = len(a)
    se = stats.sem(a)

    h = se * stats.t.ppf((1 + confidence) / 2., n - 1)
    return h

def confidence_interval(data, confidence=0.95):
    return confidence_value(data, confidence)


def formula_nalimov(x1, df):
    q = np.abs((x1 - np.average(df)) / np.std(df)) * np.sqrt(len(df) / (len(df) - 1))
    return q


def calc_q_nalimov(df):
    q = []
    for num in df:
        q.append(formula_nalimov(num, df))
    return q


def get_q_crit_nalimov(df, alpha=0.05):
    ot = nalimov_table()
    n_deg_f = len(df) - 2
    if n_deg_f < 1:
        print('not enough degrees of freedom. Make more tests!')
        print('exit program')
        exit()
    for i in range(n_deg_f, 100):
        if n_deg_f in ot.nalimov_table()['f']:
            q_crit = ot.nalimov_table()[str(alpha)][ot.nalimov_table()['f'].index(n_deg_f)]
            break
    return q_crit


def remove_outliers_nalimov(df, alpha=0.05):
    q = calc_q_nalimov(df)
    q_crit = get_q_crit_nalimov(df, alpha)
    cleaned = [val for val in q if val < q_crit]
    return cleaned


def nalimov_table():
    df = {'f': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 25, 30, 35, 40, 45, 50, 100, 200,
                300, 400, 500, 600, 700, 800, 1000],
          '0.05': [1.409, 1.645, 1.757, 1.814, 1.848, 1.87, 1.885, 1.895, 1.903, 1.91, 1.916, 1.92, 1.923, 1.926, 1.928,
                   1.931, 1.933, 1.935, 1.936, 1.937, 1.942, 1.945, 1.948, 1.949, 1.95, 1.951, 1.956, 1.958, 1.958,
                   1.959, 1.959, 1.959, 1.959, 1.959, 1.96],
          '0.01': [1.414, 1.715, 1.918, 2.051, 2.142, 2.208, 2.256, 2.294, 2.324, 2.348, 2.368, 2.385, 2.399, 2.412,
                   2.423, 2.432, 2.44, 2.447, 2.454, 2.46, 2.483, 2.498, 2.509, 2.518, 2.524, 2.529, 2.553, 2.564,
                   2.566, 2.568, 2.57, 2.571, 2.572, 2.573, 2.576],
          '0.001': [1.414, 1.73, 1.982, 2.178, 2.329, 2.447, 2.54, 2.616, 2.678, 2.73, 2.774, 2.812, 2.845, 2.874,
                    2.899, 2.921, 2.941, 2.959, 2.975, 2.99, 3.047, 3.085, 3.113, 3.134, 3.152, 3.166, 3.227, 3.265,
                    3.271, 3.275, 3.279, 3.281, 3.283, 3.285, 3.291]
          }
    return df
