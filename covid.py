# main stuff
from etl_functions import read_csv_files_to_dict, extract_confirmed_cases, \
    build_line_plot, data_to_dataframe

cases = extract_confirmed_cases(read_csv_files_to_dict())
build_line_plot(*data_to_dataframe(cases))
