# main stuff
from etl_functions import read_csv_files_to_list, extract_confirmed_cases, \
    build_line_plot, zip_dates_and_cases

cases = extract_confirmed_cases(read_csv_files_to_list())
build_line_plot(*zip_dates_and_cases(cases))
