# %% [markdown]
# # Setup

# %%
# importing required modules
import pandas as pd
from IPython.display import display
from funcs.pdf_extraction import get_pdf_totals
from funcs.data_display import display_totals, display_df_split_by_time


# %% [markdown]
# ## Validation Outputs
spend_df = get_pdf_totals(pdf_file_paths='file_paths.csv', vendor_categories="vendor_category.csv")
spend_df.to_csv('Total Costs.csv', index=False)

# %% [markdown]
# ### Receipts
display(spend_df.sort_values('total', ascending=False))

# %% [markdown]
# ## Balance
display_totals(spend_df, income_df=pd.read_csv("income.csv"), str_carry_over_tag='CarryOver')

# %% [markdown]
# ## Vendor Breakdown
display(spend_df[['vendor', 'total']].groupby('vendor').sum().sort_values('total', ascending=False))

# %% [markdown]
# ## Vendor Category Breakdown
display(spend_df.groupby('category').sum().sort_values('total', ascending=False))

# %% [markdown]
# ## Reimbursement Calculations
display_df_split_by_time(spend_df, date_cutoff='3/1/22')
