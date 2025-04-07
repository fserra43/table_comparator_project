import re
import pandas as pd

def export_comparison_to_excel(result, filename="comparison.xlsx"):
    """
    Exports the comparison result to an Excel file.
    
    If result["status"] == "ERROR", it creates an "Errors" sheet listing the error messages.
    If result["status"] == "OK", it creates:
      1. "1. Overview"
      2. "2. Column Summary" (with hyperlinks to detail sheets)
      3. Detail sheets for each column with mismatches.
    """
    if result["status"] == "ERROR":
        df_errors = pd.DataFrame({"Error Messages": result["errors"]})
        with pd.ExcelWriter(filename, engine='xlsxwriter') as writer:
            df_errors.to_excel(writer, sheet_name="Errors", index=False)
        print(f"Comparison Excel exported (errors): {filename}")
        return

    overview = result["overview"]
    discrepancies = result["discrepancies"]

    # Build Overview DataFrame
    overview_rows = []
    for category, info in overview.items():
        overview_rows.append([category, info["count"], info["sample"]])
    df_overview = pd.DataFrame(overview_rows, columns=["Category", "Count", "Sample PKs"])

    # Build Column Summary DataFrame
    summary_data = []
    for col, mismatch_list in discrepancies.items():
        total_mismatches = sum(item["count"] for item in mismatch_list)
        summary_data.append([col, total_mismatches])
    if summary_data:
        df_col_summary = pd.DataFrame(summary_data, columns=["Column", "Number of Discrepancies"])
        df_col_summary.sort_values("Number of Discrepancies", ascending=False, inplace=True)
        df_col_summary.reset_index(drop=True, inplace=True)
    else:
        df_col_summary = pd.DataFrame(columns=["Column", "Number of Discrepancies"])
    df_col_summary["Details Link"] = ""

    def sheet_name(col_name, prefix="Detail - ", max_len=31):
        safe_name = re.sub(r"[\[\]*:?/\\]", "", col_name)
        return (prefix + safe_name)[:max_len]

    with pd.ExcelWriter(filename, engine='xlsxwriter') as writer:
        # Sheet 1: Overview
        df_overview.to_excel(writer, sheet_name="1. Overview", index=False)
        # Sheet 2: Column Summary
        df_col_summary.to_excel(writer, sheet_name="2. Column Summary", index=False)
        workbook = writer.book
        summary_ws = writer.sheets["2. Column Summary"]

        # Detail sheets
        for idx, row in df_col_summary.iterrows():
            col = row["Column"]
            if pd.isna(col) or not col:
                continue
            detail_sheet = sheet_name(str(col))
            mismatch_list = discrepancies[col]
            detail_rows = []
            for item in mismatch_list:
                detail_rows.append([
                    item["table1_value"],
                    item["table2_value"],
                    item["count"],
                    item["sample"]
                ])
            df_details = pd.DataFrame(detail_rows, columns=["Table1 Value", "Table2 Value", "Count", "Sample PKs"])
            df_details.sort_values("Count", ascending=False, inplace=True)
            df_details.to_excel(writer, sheet_name=detail_sheet, index=False)
            link_formula = f'=HYPERLINK("#\'{detail_sheet}\'!A1", "Go to {col} Details")'
            df_col_summary.at[idx, "Details Link"] = link_formula

        # Rewrite Column Summary with link formulas
        df_col_summary.to_excel(writer, sheet_name="2. Column Summary", index=False)
        link_col_idx = df_col_summary.columns.get_loc("Details Link")
        for row_idx in range(len(df_col_summary)):
            formula = df_col_summary.iat[row_idx, link_col_idx]
            summary_ws.write_formula(row_idx + 1, link_col_idx, formula)

    print(f"Comparison Excel exported: {filename}")
