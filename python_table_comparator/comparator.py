import pandas as pd

def compare_tables_on_pk(table1, table2, pk, sample_size=5):
    """
    Compares two DataFrames with extra validations:
      1) The PK columns must exist in both tables.
      2) The PK must be unique in each table.
      3) Non-PK columns must match exactly.

    Returns a dictionary with the following structure:
      {
        "status": "OK" or "ERROR",
        "errors": [list of error messages],
        "overview": { ... },           # Only if status is "OK"
        "discrepancies": { ... }       # Only if status is "OK"
      }
    """
    result = {
        "status": "OK",
        "errors": [],
        "overview": {},
        "discrepancies": {}
    }
    pk_list = pk if isinstance(pk, list) else [pk]
   
    df1 = table1.copy()
    df2 = table2.copy()
    
    # 1) Check that all PK columns exist in both tables
    missing_in_1 = [c for c in pk_list if c not in df1.columns]
    missing_in_2 = [c for c in pk_list if c not in df2.columns]
    if missing_in_1 or missing_in_2:
        result["status"] = "ERROR"
        result["errors"].append(f"Missing PK columns: table1 {missing_in_1}, table2 {missing_in_2}")
        return result
    
    # 2) Check for PK uniqueness in each table
    if df1.duplicated(subset=pk_list).any():
        result["status"] = "ERROR"
        result["errors"].append("Primary key is not unique in table1.")
    if df2.duplicated(subset=pk_list).any():
        result["status"] = "ERROR"
        result["errors"].append("Primary key is not unique in table2.")
    
    # 3) Create a single PK column by concatenating the PK columns
    df1['PK'] = df1[pk_list].astype(str).agg('-'.join, axis=1)
    df2['PK'] = df2[pk_list].astype(str).agg('-'.join, axis=1)
    df1.drop(columns=pk_list, inplace=True)
    df2.drop(columns=pk_list, inplace=True)
    
    # 4) Check that the non-PK columns match exactly between both tables
    cols1 = set(df1.columns)
    cols2 = set(df2.columns)
    if cols1 != cols2:
        result["status"] = "ERROR"
        diff = cols1.symmetric_difference(cols2)
        result["errors"].append(f"Non-PK columns differ: {sorted(diff)}")
    
    # If there are any errors, return the result immediately
    if result["status"] == "ERROR":
        return result

    # Reorder columns in a consistent order
    common_cols_sorted = sorted(list(cols1))
    df1 = df1[common_cols_sorted]
    df2 = df2[common_cols_sorted]
    
    # 5) Set 'PK' as index
    df1.set_index('PK', inplace=True)
    df2.set_index('PK', inplace=True)
    
    # 6) Determine row memberships
    keys1 = set(df1.index)
    keys2 = set(df2.index)
    only_in_1 = keys1 - keys2
    only_in_2 = keys2 - keys1
    common_keys = keys1 & keys2
    
    df1_common = df1.loc[list(common_keys)].sort_index()
    df2_common = df2.loc[list(common_keys)].sort_index()
    
    equal_mask = df1_common.eq(df2_common).all(axis=1)
    same_rows = set(df1_common.index[equal_mask])
    diff_rows = common_keys - same_rows
    
    overview = {
        "only_in_table1": {
            "count": len(only_in_1),
            "sample": ", ".join(list(only_in_1)[:sample_size])
        },
        "only_in_table2": {
            "count": len(only_in_2),
            "sample": ", ".join(list(only_in_2)[:sample_size])
        },
        "common_different": {
            "count": len(diff_rows),
            "sample": ", ".join(list(diff_rows)[:sample_size])
        },
        "common_same": {
            "count": len(same_rows),
            "sample": ", ".join(list(same_rows)[:sample_size])
        }
    }
    
    discrepancies = {}
    if diff_rows:
        df1_diff = df1_common.loc[list(diff_rows)]
        df2_diff = df2_common.loc[list(diff_rows)]
        for col in df1_diff.columns:
            mismatch_mask = df1_diff[col] != df2_diff[col]
            mismatch_pks = df1_diff[mismatch_mask].index
            if mismatch_pks.empty:
                continue
            grouping = {}
            for pk_val in mismatch_pks:
                val1 = df1_diff.loc[pk_val, col]
                val2 = df2_diff.loc[pk_val, col]
                pair = (str(val1), str(val2))
                grouping.setdefault(pair, []).append(pk_val)
            mismatch_list = []
            for (val1, val2), pk_vals in grouping.items():
                mismatch_list.append({
                    "table1_value": val1,
                    "table2_value": val2,
                    "count": len(pk_vals),
                    "sample": ", ".join(pk_vals[:sample_size])
                })
            discrepancies[col] = mismatch_list
    
    result["overview"] = overview
    result["discrepancies"] = discrepancies
    return result