import os
import os.path


def _scan_file(input_regx_list, input_file):
    """
    This function gets the list of statements matching the regular expressions
    provided through input_regx_list

    :param input_regx_list: list of regular expressions used for extracting statements with import key words
    :param input_file: input file 
    :return: list of pythoh statements matching the input_regx_list in the input_file
    """
    import re
    list_lines = []
    try:
        fp = open(input_file)
        file_data = fp.readlines()
        for line in file_data:
            for reg_ex in input_regx_list:
                if re.match(reg_ex, line, re.I):
                    list_lines.append(line)
        fp.close()
    except IOError as exp:
        print("Exception :", str(exp))

    return list_lines


def _get_modules_from_file(file_path):
    """
    This function gets list of modules used in the python script file_path

    :param: file_path - path to python script
    :return: a dictionary object of the form {file_path : [module names]}
    """
    import re
    regx_list = [r'\s*import\s*.*', r'\s*from\s*\S+.*']
    list_lines = _scan_file(regx_list, file_path)
    module_list = []
    if list_lines:
        for item in list_lines:
            item = item.strip()
            if re.match(r'from', item):         # checking for import statements of the form 'from module import ...'
                words = item.split()
                module_list.append(words[1])
            elif re.match(r'import', item):	    # checking for import statements of the form 'import module'
                words = item.split()
                module_list.append(words[1])
    module_set = set(module_list)
    module_list = list(module_set)
    return {file_path: module_list}


def _dir_list(dir_path):
    """
    This function gets the dir entries in the dir_path

    :param: dir_path - path to directory
    :return: a list of path objects
    """
    import pathlib

    path_list = pathlib.Path(dir_path).glob('**/*')
    return path_list


def _get_modules_from_files_in_directory(dir_path):
    """
    This function gets the list of module names for each python script in the dir_path

    :param: dir_path - path to a directory
    :return: a dictionary object of the form {file_path1 : [module_names], file_path2 : [module_names] ... }
    """
    temp_module_list_dict = {}
    path_list = _dir_list(dir_path)
    for path_item in path_list:
        if not os.path.isfile(str(path_item)):
            continue
        if str(path_item).endswith(".py"):
            x = _get_modules_from_file(str(path_item))
            temp_module_list_dict.update(x)

    return temp_module_list_dict


def get_module_names(file_or_dir_path):
    """
    This function gets the list of module names used in given python script or in all the python
    scripts in the specified path
    """

    if not os.path.exists(file_or_dir_path):
        raise Exception("File or Directory not found")

    if os.path.isfile(file_or_dir_path):
        module_list_dict = _get_modules_from_file(file_or_dir_path)
    else:
        module_list_dict = _get_modules_from_files_in_directory(file_or_dir_path)

    return module_list_dict
