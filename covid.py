# main stuff
import get_new_csv
from etl_functions import read_csv_files_to_dict, \
    extract_confirmed_cases_deaths_recovered, \
    build_line_plot, data_to_dataframe

# get_new_csv.main()
cases = extract_confirmed_cases_deaths_recovered(read_csv_files_to_dict(),
                                                 "china")
build_line_plot(*data_to_dataframe(cases))
