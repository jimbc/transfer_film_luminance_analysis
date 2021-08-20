from __future__ import print_function
import re
import glob
import os


########################## file operations ###############################

def file_open(filename, encoding='iso-8859-1'):
    f = open(filename, encoding=encoding)
    file_data = f.readlines()
    f.close()
    return file_data


def read_file(fn, enc):
    return file_open(fn, enc)


def read_table(file_src, encoding='iso-8859-1', dropfirst=None, sep=None):
    with open(file_src, encoding=encoding) as f:
        data = [line.split(sep) for line in f.readlines()]
        data = data[dropfirst:]
    return data


def read_yaml(filepath):
    import yaml
    with open(filepath) as f:
        file_data = yaml.load(f, Loader=yaml.CLoader)
    return file_data


def read_json(file_src):
    import json
    with open(file_src) as json_file:
        file_data = json.load(json_file)
    return file_data


def to_yaml(data_file, filepath):
    import yaml
    with open(filepath, 'w+') as f_out:
        f_out.write(yaml.dump(data_file))
    return


def to_json(data_file, dst_src):
    import json
    with open(dst_src, 'w+') as f_out:
        f_out.write(json.dumps(data_file))


# def fname_lst_of_dir(directorypath=".", ext=''):
#     list_of_files = glob.glob(directorypath + '*' + ext)
#     return list_of_files


# def date_sorted_fname_lst_of_dir(directorypath="."):
#     list_of_files = fname_lst_of_dir(directorypath)
#     list_of_files = sorted(list_of_files, key=os.path.getmtime)
#     return list_of_files


# def newest_file(filepath='.'):
#     list_of_files = glob.glob(filepath + "*")
#     for file in list_of_files:
#         if os.path.isfile(file) == False:
#             list_of_files.remove(file)
#     newest_file = max(list_of_files, key=os.path.getctime)
#     _, filename = os.path.split(newest_file)
#     return filename


def get_list_of_directories(path):
    listfiles = []
    for el in os.listdir(path):
        if os.path.isdir(el):
            listfiles.append(el)
    return listfiles


def get_list_of_filenames(src='.', ext='txt', verbose=False):
    listfiles = []
    for file in os.listdir(src):
        if file.endswith("." + ext):
            listfiles.append(file)
    if verbose:
        if listfiles:
            print("found files: ")
            for i in range(0, len(listfiles)):
                print(listfiles[i])
            print("#" * 60)
        else:
            # later replace with raise cmd
            print("No files found!")
            print("Process is terminated!")
            exit()
    return listfiles


################################### data initialize operations ######################################

def list_to_table(df):
    "converts an 1-dimensional list of quantities with separators into a 2-dimensional list"
    rv = [line.split() for line in df]
    return rv


# def split_header_and_data(file_data, data_seperator='\t'):
#     i = 0
#     for line in file_data:
#         if re.search('\d+.\d+' + data_seperator + '\d+.\d+' + data_seperator, line):
#             break
#         i += 1
#     header_data = file_data[0:i]
#     value_data = file_data[i:]
#     return value_data, header_data


# def get_data(file_data):
#     data = split_header_and_data(file_data)[0]
#     return data


# def get_header(file_data):
#     header = split_header_and_data(file_data)[1]
#     return header


# def convert_data_to_float_array(value_data):
#     data_array = []
#     # to avoid wrong pattern in last line:
#     value_data.pop()
#     for line in value_data:
#         data_line = line.split("\t")
#         data_line_array = []
#         data_line.pop()  # remove \n
#         for data_point in data_line:
#             # print(data_point)
#             if '_' in data_point:
#                 data_line_array.append(data_point)
#             elif 'None' in data_point:
#                 data_line_array.append(0)
#             else:
#                 data_line_array.append(float(data_point))
#         data_array.append(data_line_array)
#     return data_array


# def floats(string):
#     floats = re.findall(r"[-+]?\d*\.\d+|\d+", string)
#     floats = [float(f) for f in floats]
#     if len(floats) == 1:
#         floats = floats[0]
#     return floats


def get_column(data_array, column):
    column_array = [line[column] for line in data_array]
    return column_array


def append_column(data_array, column):
    i = 0
    for row in data_array:
        row.append(column[i])
        i += 1
    return data_array


# def create_label_dct(header_data, label_seperator='\t'):
#     labels = header_data[-1].split(label_seperator)
#     labels.pop()
#     label_dct = {}
#     i = 0
#     for name in labels:
#         label_dct[name] = i
#         i += 1
#     return label_dct


# def create_values_dct(label_dct, data_array):
#     data_dct = {}
#     for label in label_dct:
#         data_dct[label] = (get_column(data_array, label_dct[label]))
#     return data_dct


# def create_data_header_dct(filename, filepath, label_separator='\t', data_seperator='\t'):
#     file_data = file_open(filename, filepath)
#     value_data, header_data = split_header_and_data(file_data, data_seperator)
#     header_dct = get_header_information_dct(header_data)
#     data_array = convert_data_to_float_array(value_data)
#     label_dct = create_label_dct(header_data, label_separator)
#     data_dct = create_values_dct(label_dct, data_array)
#     return data_dct, header_dct


def float_list(fn, dec='.'):
    """casts a list of characters into a list of floats
    """

    if not dec == '.':
        return [[float(s.replace(dec, '.')) for s in line] for line in fn]
    else:
        return [[float(s) for s in line] for line in fn]


def float_table(df):
    """
    cast a two-dimensional list of string numbers into floats
    :param df: 2 dimensional set of string numbers
    :return: df
    """
    outer = []
    for line in df:
        inner = []
        for s in line:
            if s is not '':
                inner.append(float(s))
            else:
                pass
                inner.append(s)
        outer.append(inner)
    return outer


def remove_non_numbers(array):
    res = [el for el in array if type(el) == int or type(el) == float]
    return res


######################## atlas operations ###########################################
def read_proc_file(fn, skip_lines=1, sep='\t'):
    df = read_table(fn, sep=sep)
    df = df[skip_lines:]
    for i in range(len(df)):
        df[i][-1] = df[i][-1].replace('\n', '')  # removes newline in df
    return df


######################## math operations ###########################################

def vector_add(vector, value):
    """
    adds a number value to every element in a dimensional list and return a one-dimensional list
    vector	1-dimensional list
    value	number value
    """
    # if type(vector) in not list:
    new_vector = [f + value for f in vector]
    return new_vector


def vector_multiply(vector, value):
    """
    multiply a number value to every element in a dimensional list and return a one-dimensional list

    vector	1-dimensional list
    value	number value
    """

    # if type(vector) in not list:
    new_vector = [f * value for f in vector]
    return new_vector


def matrix_add_value(matrix, i_col, value):
    """adds a value to every element in a column of a matrix

    matrix	two-dimensional list\
    i_col	column index of type int
    value	number value
    """

    col = get_column(matrix, i_col)
    col = vector_add(col, value)
    m = edit_column_in_matrix(matrix, i_col, col)
    return m


def edit_column_in_matrix(matrix, i_col, col):
    """
    replace a one-dimensional column in matrix with a another one-dimension column
    matrix	two-dimensional list
    i_col	index of matrix that is edited
    col		list of new column values which are replace at list index i_col
    """
    i = 0
    for row in matrix:
        row[i_col] = col[i]
        i += 1
    return matrix


######################## specific file header operations #########################################

def roundregex(value, n):
    value = value[0]
    value = float(value)
    value = round(value, n)
    # value = str(value)
    return value


def get_header_information_dct(header_data):
    header_inf_dct = {}
    for line in header_data:
        key_value = re.findall('(.+) =\t(.+)', line)
        if key_value:
            header_inf_dct[key_value[0][0]] = key_value[0][1]
    return header_inf_dct


######################## dct operations ################################

def create_index_for_datapoints(data_dct):
    # global index
    index = []
    for i in range(0, len(list(data_dct.values())[0])):
        index.append(i)
    data_dct['index'] = index
    return data_dct


######################## machine specific operations#########################
def frt_write_surface_file(df, fn):
    outfile = open(fn, 'w')
    last = df[0][1]
    for line in df:
        if last != line[1]:
            outfile.write('\n')
            last = line[1]
        s = '{}\t{}\t{}\n'.format(str(line[1] * 1e3), str(line[0] * 1e3), str(line[2] * 1e6))
        outfile.write(s)
    outfile.close()
    return


def frt_write_line_file(df, fn):
    outfile = open(fn, 'w')
    for line in df:
        s = '{}\t{}\n'.format(str(line[0] * 1e3), str(line[1] * 1e3))
        outfile.write(s)
    outfile.close()
    return
