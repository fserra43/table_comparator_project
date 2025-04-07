import os
import pandas as pd
import seaborn as sns
import numpy as np

# Import package functions (assuming the package was installed in editable mode)
from python_table_comparator.comparator import compare_tables_on_pk
from python_table_comparator.exporter import export_comparison_to_excel

# Create the "reports" folder if it does not exist
REPORTS_FOLDER = "reports"
os.makedirs(REPORTS_FOLDER, exist_ok=True)

def run_diamonds_example():
    # Example using the "diamonds" dataset from seaborn
    diamonds = sns.load_dataset("diamonds")
    diamonds = diamonds.reset_index().rename(columns={"index": "diamond_id"})
    
    df1 = diamonds.copy()
    df2 = diamonds.copy()
    df2 = df2[df2["diamond_id"] >= 5000].copy()
    
    # Add new rows to simulate differences
    new_rows = []
    start_new_id = 60000
    for i in range(100):
        new_rows.append({
            "diamond_id": start_new_id + i,
            "carat": 2.5,
            "cut": "Ideal",
            "color": "E",
            "clarity": "SI2",
            "depth": 62.0,
            "table": 58.0,
            "price": 9999,
            "x": 8.1,
            "y": 8.1,
            "z": 5.0
        })
    df2 = pd.concat([df2, pd.DataFrame(new_rows)], ignore_index=True)
    
    rng = np.random.default_rng(seed=42)
    common_ids = set(df1["diamond_id"]) & set(df2["diamond_id"])
    common_ids_list = list(common_ids)
    rng.shuffle(common_ids_list)
    selected_ids = common_ids_list[:200]
    
    numeric_cols = ["carat", "depth", "table", "price", "x", "y", "z"]
    categorical_cols = ["cut", "color", "clarity"]
    
    for pk_val in selected_ids:
        if rng.random() < 0.5:
            col_to_change = rng.choice(numeric_cols)
            old_value = df2.loc[df2["diamond_id"] == pk_val, col_to_change]
            if not old_value.empty:
                if col_to_change == "price":
                    df2.loc[df2["diamond_id"] == pk_val, col_to_change] = old_value + 123
                else:
                    df2.loc[df2["diamond_id"] == pk_val, col_to_change] = old_value * 1.1
        else:
            col_to_change = rng.choice(categorical_cols)
            if col_to_change == "cut":
                df2.loc[df2["diamond_id"] == pk_val, col_to_change] = "Premium"
            elif col_to_change == "color":
                df2.loc[df2["diamond_id"] == pk_val, col_to_change] = "F"
            elif col_to_change == "clarity":
                df2.loc[df2["diamond_id"] == pk_val, col_to_change] = "VS1"
    
    # In this example, "diamond_id" is used as the PK
    result_diamonds = compare_tables_on_pk(df1, df2, pk="diamond_id")
    export_comparison_to_excel(result_diamonds, os.path.join(REPORTS_FOLDER, "diamonds_comparison.xlsx"))

if __name__ == "__main__":
    run_diamonds_example()