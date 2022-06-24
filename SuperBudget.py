# %% [markdown]
# # Setup

# %%
# importing required modules
import pandas as pd
from IPython.display import display
from funcs.pdf_extraction import get_pdf_totals

# Set dataframes to always show 2 decimal places
pd.options.display.float_format = "{:.2f}".format

# %% [markdown]
# ## Validation Outputs
spend_df = get_pdf_totals(pdf_file_paths='file_paths.csv', vendor_categories="vendor_category.csv")
spend_df.to_csv('Total Costs.csv', index=False)

display(spend_df.sort_values('total', ascending=False))

# %% [markdown]
# ## Balance
income_df = pd.read_csv("income.csv")
carry_over_mask = (income_df['sponsor'] == 'CarryOver')
print('+ Total Income:\t\t %.2f' % income_df['amount'].sum())
print('\t| New Income\t %.2f' % income_df.loc[~carry_over_mask]['amount'].sum())
print('\t| Carry Over\t %.2f' % income_df.loc[carry_over_mask]['amount'].sum())
print('- Total Spent:\t\t %.2f' % spend_df['total'].sum())
print('===================')
print('Remaining Balance:\t %.2f' % (income_df['amount'].sum()-spend_df['total'].sum()))

# %% [markdown]
# ## Vendor Breakdown
display(spend_df[['vendor', 'total']].groupby(
    'vendor').sum().sort_values('total', ascending=False))

# %% [markdown]
# ## Vendor Category Breakdown
display(spend_df.groupby('category').sum(
).sort_values('total', ascending=False))

# %% [markdown]
# ## Reimbursement Calculations
date_cutoff = '3/1/22'

# %%
pre_cuttoff_df = spend_df.loc[spend_df['date'] < date_cutoff]
print(pre_cuttoff_df['total'].sum())
display(pre_cuttoff_df)

# %%
post_cuttoff_df = spend_df.loc[spend_df['date'] >= date_cutoff]
print(post_cuttoff_df['total'].sum())
display(post_cuttoff_df)
