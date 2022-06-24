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
df = get_pdf_totals('file_paths.csv')
df.to_csv('Total Costs.csv', index=False)

display(df.sort_values('total', ascending=False))

# %% [markdown]
# ## Balance
income_df = pd.read_csv("income.csv")

total_income = income_df['amount'].sum()
new_income = income_df.loc[income_df['sponsor'] != 'CarryOver']['amount'].sum()
carryover_income = income_df.loc[income_df['sponsor'] == 'CarryOver']['amount'].sum()
total_spent = df['total'].sum()
remaining_balance = total_income - total_spent

print('+ Total Income:\t\t %.2f' % total_income)
print('\t| New Income\t %.2f' % new_income)
print('\t| Carry Over\t %.2f' % carryover_income)
print('- Total Spent:\t\t %.2f' % total_spent)
print('===================')
print('Remaining Balance:\t %.2f' % remaining_balance)

# %% [markdown]
# ## Vendor Breakdown
display(df[['vendor', 'total']].groupby(
    'vendor').sum().sort_values('total', ascending=False))

# %% [markdown]
# ## Vendor Category Breakdown
cat_df = df.merge(pd.read_csv("vendor_category.csv"), on="vendor")
display(cat_df.groupby('category').sum(
).sort_values('total', ascending=False))

# %% [markdown]
# ## Reimbursement Calculations
date_cutoff = '3/1/22'

# %%
pre_cuttoff_df = df.loc[df['date'] < date_cutoff]
print(pre_cuttoff_df['total'].sum())
display(pre_cuttoff_df)

# %%
post_cuttoff_df = df.loc[df['date'] >= date_cutoff]
print(post_cuttoff_df['total'].sum())
display(post_cuttoff_df)
