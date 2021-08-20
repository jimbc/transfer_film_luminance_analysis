import os


########################## file operations ###############################
def read_yaml(file_path):
    import yaml
    with open(file_path) as yaml_file:
        file_data = yaml.load(yaml_file, Loader=yaml.CLoader)
    return file_data


def to_yaml(dict_file, file_path):
    import yaml
    with open(file_path, 'w+') as f_out:
        f_out.write(yaml.dump(dict_file))
    return


def read_json(file_path):
    import json
    with open(file_path) as json_file:
        file_data = json.load(json_file)
    return file_data


def to_json(dict_file, file_path):
    import json
    with open(file_path, 'w+') as f_out:
        f_out.write(json.dumps(dict_file))
    return

def read_atlas(file_path):
    import read_atlas
    df = read_atlas.AtlasData(file_path)
    return df


def get_list_of_directories(path):
    list_dirs = []
    for el in os.listdir(path):
        if os.path.isdir(el):
            list_dirs.append(el)
    return list_dirs


def get_list_of_filenames(src='.', ext='txt'):
    list_files = []
    for file in os.listdir(src):
        if file.endswith(ext):
            list_files.append(file)
    return list_files


################################### data initialize operations ######################################

def list_to_table(df):
    "converts an 1-dimensional list of quantities with separators into a 2-dimensional list"
    rv = [line.split() for line in df]
    return rv


def get_column(data_array, column):
    column_array = [line[column] for line in data_array]
    return column_array


def append_column(data_array, column):
    i = 0
    for row in data_array:
        row.append(column[i])
        i += 1
    return data_array


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


######################## atlas operations ##########################################


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
