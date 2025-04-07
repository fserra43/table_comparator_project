import os
import pandas as pd
import seaborn as sns

# Import package functions (assuming the package was installed in editable mode)
from python_table_comparator.comparator import compare_tables_on_pk
from python_table_comparator.exporter import export_comparison_to_excel

# Create the "reports" folder if it does not exist
REPORTS_FOLDER = "reports"
os.makedirs(REPORTS_FOLDER, exist_ok=True)

def run_simple_examples():
    # Example 1: Scenario with valid data
    data1 = {
        'id': [1, 2, 3],
        'country': ['ES', 'FR', 'IT'],
        'value': [10, 20, 30]
    }
    data2 = {
        'id': [2, 3, 4],
        'country': ['FR', 'IT', 'GR'],
        'value': [20, 25, 999]
    }
    df1 = pd.DataFrame(data1)
    df2 = pd.DataFrame(data2)
    
    # Call the function passing the PK (you can pass a single column or a list)
    result = compare_tables_on_pk(df1, df2, pk='id')
    
    # Export the result to Excel
    export_comparison_to_excel(result, os.path.join(REPORTS_FOLDER, "comparison_valid.xlsx"))

    # Example 2: Failing scenario (duplicated PK in table1)
    data_fail = {
        'id': [2, 2, 3],
        'country': ['FR', 'FR', 'IT'],
        'value': [20, 25, 30]
    }
    df_fail = pd.DataFrame(data_fail)
    result_fail = compare_tables_on_pk(df_fail, df2, pk='id')
    export_comparison_to_excel(result_fail, os.path.join(REPORTS_FOLDER, "comparison_errors.xlsx"))


if __name__ == "__main__":
    run_simple_examples()