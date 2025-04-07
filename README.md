# Python Table Comparator

This repository contains the complete code for a custom table comparator in Python. It serves as the code base for my Medium article **"Building a Custom Table Comparator in Python (and How to Apply It to Real Datasets)"**.

The table comparator compares two pandas DataFrames based on a specified primary key (PK). It performs the following tasks:

1. **Primary Key Validation and Creation**  
    - **PK Existence Check:** Verifies that the specified PK columns exist in both DataFrames.  
    - **PK Uniqueness Check:** Ensures that the primary key is unique within each table.  
    - **PK Concatenation:** Combines one or more PK columns into a single string (using hyphens) and sets it as the DataFrame index.

2. **Column Alignment Check**  
    - After removing the original PK columns, it checks that both DataFrames have the exact same set of non-PK columns. If not, it marks the comparison as an error.

3. **Row-Level Comparison**  
    - Using set operations on the PK index, the comparator determines which rows are exclusive to each DataFrame and which rows are common.  
    - For the common rows, it checks whether all column values match.

4. **Column-Level Discrepancy Analysis**  
    - For common rows that differ, the comparator examines each column individually.  
    - It groups mismatches by the differing values (from table 1 and table 2) and counts their occurrences.

5. **Excel Report Generation**  
    - If any validation fails, the comparator returns an error status and the Excel export function creates a single **"Errors"** sheet listing the issues.  
    - Otherwise, it produces a multi-sheet Excel report that includes:
        - **"1. Overview":** A summary of row presence (only in table 1, only in table 2, common and identical, common but different).  
        - **"2. Column Summary":** A list of columns with the total number of discrepancies, with clickable hyperlinks leading to the detail sheets.  
        - **Detail Sheets:** One sheet per column showing the specific mismatches (the paired values, their counts, and a sample of the PKs).

## Repository Structure
```bash
table_comparator_project/            # Project root directory
├── reports/                         # Folder for generated reports (Excel)
│   └── (output files are saved here)
├── python_table_comparator/         # Main package containing the comparison logic
│   ├── __init__.py                  # Package initializer
│   ├── comparator.py                # Function: compare_tables_on_pk
│   └── exporter.py                  # Function: export_comparison_to_excel
├── examples/                        # Usage examples for the package
│   └── usage_example.py             # Script with comparison examples
├── setup.py                         # Project configuration (optional)
├── README.md                        # Project documentation
└── LICENSE                          # License file


```


## Detailed Explanation of Key Functions

### `compare_tables_on_pk(table1, table2, pk, sample_size=5)`

- **Purpose:**  
    Compares two DataFrames with extra validations.

- **Arguments:**
    - `table1`: A pandas DataFrame representing the first dataset.
    - `table2`: A pandas DataFrame representing the second dataset.
    - `pk`: A string (or list of strings) specifying the column(s) that form the primary key.
    - `sample_size` (optional): An integer (default 5) that defines how many primary key values to include as a sample in the output.

- **Returns:**  
    A dictionary with the following structure:
    ```python
    {
        "status": "OK" or "ERROR",
        "errors": [list of error messages],  # Only if status is "ERROR"
        "overview": { ... },                 # Present only if status is "OK"
        "discrepancies": { ... }             # Present only if status is "OK"
    }
    ````

### `export_comparison_to_excel(result, filename="comparison.xlsx")`
- **Purpose:**  
    Exports the result of the comparison to an Excel file.

- **Arguments:**
    - `result`: The dictionary returned by `compare_tables_on_pk()`.
    - `filename` (optional): The name of the Excel file to create (default is `"comparison.xlsx"`).

- **Behavior**:
    - If `result["status"]` is `"ERROR"`, the function creates an Excel file with a single sheet named **"Errors"** that lists all error messages.
    - If `result["status"]` is `"OK"`, it generates a multi-sheet Excel file that includes:
        - **"1. Overview"**: A summary of the row-level comparison.
        - **"2. Column Summary"**: A sheet with the total number of discrepancies per column, including clickable hyperlinks to detail sheets.
        - **Detail Sheets**: One sheet per column that has mismatches, showing the specific differences, counts, and sample primary keys.

## Getting Started

1. **Clone the Repository:**
    ```bash
    git clone https://github.com/your-username/table_comparator_project.git
    cd table_comparator_project
    ````

2. **Create a Virtual Environment:**
    It is recommended to create a virtual environment to isolate project dependencies.
    - On Linux/macOS:
    ```bash
    python3 -m venv venv
    source venv/bin/activate
    ````

    - On Windows:
    ```bash
    python3 -m venv venv
    .\venv\Scripts\activate
    ````

3. **Installing the Package**
    Install the package in editable mode so that any changes you make are reflected immediately:
    ```bash
    pip install -e .
    ````

4. **Run the Usage Example**
    This script introduces two very basic examples to illustrate how the comparator works. One has valid data, while the other fails due to duplicate PKs. From the repository root, run:
    ```bash
    python examples/usage_example.py
    ````
    
    This will generate Excel files in the `reports` directory:

    - `comparison_valid.xlsx` (for valid data)

    - `comparison_errors.xlsx` (if there are validation errors)

5. **Run the Diamonds Example**
    This script contains the code for the example discussed in the article **"Building a Custom Table Comparator in Python (and How to Apply It to Real Datasets)"**.  From the repository root, run:
    ```bash
    python examples/diamonds_example.py
    ````

    This will generate `diamonds_comparison.xlsx`
    
## Future Enhancements
Possible future improvements include:
- Advanced Excel formatting (e.g., conditional highlighting, auto-sizing columns).
- A hash-based method for multi-column PKs to avoid string collisions.
- Scaling the comparator for extremely large datasets using chunk processing or libraries like Polars (explored as a future possibility).

Feel free to fork, adapt, or extend the code for your own data validation needs.

Happy comparing!