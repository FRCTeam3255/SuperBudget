# %% [markdown]
# # Setup

# %%
# importing required modules
import pandas as pd
from IPython.display import display
from SuperBudget import get_pdf_totals, display_totals, display_df_split_by_time


# %% [markdown]
# ## Validation Outputs
df_spend = get_pdf_totals(pdf_file_paths='file_paths.csv', vendor_categories="vendor_category.csv")
df_spend.to_csv('Total Costs.csv', index=False)

# %% [markdown]
# ### Receipts
display(df_spend.sort_values('total', ascending=False))

# %% [markdown]
# ## Balance
display_totals(df_spend=df_spend, df_income=pd.read_csv("income.csv"), str_carry_over_tag='CarryOver')

# %% [markdown]
# ## Vendor Breakdown
display(df_spend[['vendor', 'total']].groupby('vendor').sum().sort_values('total', ascending=False))

# %% [markdown]
# ## Vendor Category Breakdown
display(df_spend.groupby('category').sum().sort_values('total', ascending=False))

# %% [markdown]
# ## Reimbursement Calculations
display_df_split_by_time(df_spend=df_spend, date_cutoff='3/1/22')
