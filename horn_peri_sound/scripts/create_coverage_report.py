
"""This file contains the logic to display aggregated coverage of
all testcases taking input as multiple coverage data files..
"""


import json
import os
import logging
import re
import vlab


def update_totals(data):
    # Extract totals information
    totals_info = data[-1].split('|')
    total_functions, total_functions_covered = map(int, totals_info[1].strip().split()[0].split('/'))
    total_statements, total_statements_covered = map(int, totals_info[2].strip().split()[0].split('/'))

    # Subtract the functions and statements covered by specific files
    files_to_subtract = ['(Unknown)', 'main.c', 'print.c', 'start.850']
    patterns = ["Mfx.*", "Mfl.*", "Ifx.*", "Ifl.*", "Efx.*"]
    regex_patterns = [re.compile(pattern) for pattern in patterns]
    functions_to_subtract = []
    statements_to_subtract = []
    func_cov_to_subtract = []
    stmt_cov_to_subtract = []

    for line in data[:-1]:
        file_name = line.split('|')[0].strip()
        if file_name in files_to_subtract or any(pattern.match(file_name) for pattern in regex_patterns):
            info = line.split('|')
            if info[1].strip() != '(Not available)':
                total_func = info[1].strip().split()[0].split('/')[1]
                total_func_cov = info[1].strip().split()[0].split('/')[0]
            else:
                total_func = 0
                total_func_cov = 0
            if info[2].strip() != '(Not available)':
                total_stmt = info[2].strip().split()[0].split('/')[1]
                total_stmt_cov = info[2].strip().split()[0].split('/')[0]
            else:
                total_stmt = 0
                total_stmt_cov = 0
            functions_to_subtract.append(int(total_func))
            func_cov_to_subtract.append(int(total_func_cov))
            statements_to_subtract.append(int(total_stmt))
            stmt_cov_to_subtract.append(int(total_stmt_cov))

    total_functions_covered -= sum(functions_to_subtract)
    total_functions -= sum(func_cov_to_subtract)
    total_statements_covered -= sum(statements_to_subtract)
    total_statements -= sum(stmt_cov_to_subtract)

    # Update the Totals line
    func_percent = round(float(total_functions) / float(total_functions_covered), 2)
    stmt_percent = round(float(total_statements) / float(total_statements_covered), 2)
    totals_info[1] = "\t{}/{}\t   {:.0%} ".format(total_functions, total_functions_covered, func_percent)
    totals_info[2] = "   {}/{}\t{:.0%} ".format(total_statements, total_statements_covered, stmt_percent)
    data[-1] = '|'.join(totals_info)

    return data


def get_xml_files(dir_path):
    files_names = [file for file in os.listdir(dir_path) if file.endswith(".xml")]
    xml_files = [os.path.join(dir_path, file) for file in files_names]
    logging.info("xml_files: %s", xml_files)
    return xml_files


def get_elf_file_names(elf_filepaths):
    with open(elf_filepaths, "r") as file:
        data = file.read().rstrip()
    return data


def map_source_path(file_path):
    # Read the content from the text file
    with open(file_path, 'r') as file:
        content = file.read()

    # Use json.loads to convert the string into a dictionary
    data_dict = json.loads(content)
    logging.info("Data dictionary for annotation: %s", data_dict)
    elf_keys_list = list(data_dict.keys())
    values_list = [tuple(value[0]) for key, value in data_dict.items()]
    vlab.source_path_map[elf_keys_list[0]] = [values_list[0]]
    new_dict = {}
    for key, value in data_dict.items():
        new_dict[key] = [tuple(value[0])]
    vlab.set_preferences(source_path_map=new_dict)


if __name__ == "__main__":
    output_file = os.environ['coverage_folder']+"/aggregated_coverage.txt"
    updated_agg_cov_file = os.environ['coverage_folder']+"/updated_aggregated_coverage.txt"
    elf_filepaths = os.environ['coverage_folder'] + '/elf_file_names.txt'
    configure_view = vlab.analysis.view.code_coverage(
            datafiles=get_xml_files(os.environ['coverage_folder']), output=output_file
    )
    elf_file_names = get_elf_file_names(elf_filepaths)
    logging.info("The aggregated coverage data below pertains to the following elf files:")
    for item in elf_file_names.split(','):
        logging.info(item)
    vlab.display_analysis(configure_view)
    if int(os.environ['GEN_COVERAGE']) == 1:
        annot_file = os.environ['coverage_folder'] + '/annot_dictionary.txt'
        map_source_path(annot_file)

    with open(output_file, 'r') as file:
        data = file.readlines()

    # Update Totals line
    updated_data = update_totals(data)

    # Save the updated data back to the text file
    with open(updated_agg_cov_file, 'w') as file:
        file.writelines(updated_data)
    vlab.exit()
