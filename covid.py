# main stuff
import get_new_csv
from etl_functions import read_csv_files_to_dict, extract_confirmed_cases, \
    build_line_plot, data_to_dataframe

# get_new_csv.main()
cases = extract_confirmed_cases(read_csv_files_to_dict())
build_line_plot(*data_to_dataframe(cases))
