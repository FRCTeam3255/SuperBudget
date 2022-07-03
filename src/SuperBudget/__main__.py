# importing required modules
import pandas as pd
from IPython.display import display
from .pdf_extraction import get_pdf_totals
from .data_display import display_totals


def main(pdf_file_paths='file_paths.csv', vendor_categories="vendor_category.csv", income_csv_file: str = "income.csv", str_carry_over_tag='CarryOver'):
    df_spend = get_pdf_totals(pdf_file_paths=pdf_file_paths, vendor_categories=vendor_categories)
    df_spend.to_csv('Total Costs.csv', index=False)

    print('\n\n', '='*5, 'Receipts', '='*5)
    display(df_spend.sort_values('total', ascending=False))

    print('\n\n', '='*5, 'Balance', '='*5)
    display_totals(df_spend=df_spend, df_income=pd.read_csv(income_csv_file), str_carry_over_tag=str_carry_over_tag)

    print('\n\n', '='*5, 'Vendor Breakdown', '='*5)
    display(df_spend[['vendor', 'total']].groupby('vendor').sum().sort_values('total', ascending=False))

    print('\n\n', '='*5, 'Vendor Category Breakdown', '='*5)
    display(df_spend.groupby('category').sum().sort_values('total', ascending=False))

    return df_spend


if __name__ == "__main__":
    print('='*8, 'Running SuperBudget', '='*8)
    main()
