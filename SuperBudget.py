# %% [markdown]
# # Setup

# %%
# importing required modules
import pandas as pd
from IPython.display import display
from funcs.pdf_extraction import load_pdf_file_totals_to_df


# %% [markdown]
# # Configuration
# Read in file paths (ignoring # comments found in file)
file_paths = pd.read_csv(
    'file_paths.csv',
    comment='#',  # comment
    index_col=0,
    header=None,
).index.to_list()


# %% [markdown]
# # Run

# %%

# %%
df = load_pdf_file_totals_to_df(file_paths)
df.to_csv('Total Costs.csv')


# %% [markdown]
# ## Validation Outputs

# %%
df.sort_values('total', ascending=False)  # .to_csv('items.csv')

# %% [markdown]
# # Analysis Outputs

# %% [markdown]
# ## Balance

# %%
income_df = pd.read_csv("income.csv")
print('+ Total Income:\t\t', income_df['amount'].sum())
print('\t| New Income\t',
      income_df.loc[income_df['sponsor'] != 'CarryOver']['amount'].sum())
print('\t| Carry Over\t',
      income_df.loc[income_df['sponsor'] == 'CarryOver']['amount'].sum())
print('- Total Spent:\t\t', round(df['total'].sum(), 0))
print('===================')
print('Remaining Balance:\t', round(
    income_df['amount'].sum() - df['total'].sum(), 0))

# %% [markdown]
# ## Vendor Breakdown

# %%
df[['vendor', 'total']].groupby(
    'vendor').sum().sort_values('total', ascending=False)

# %% [markdown]
# ## Vendor Category Breakdown

# %%
cat_df = df.merge(pd.read_csv("vendor_category.csv"), on="vendor")
cat_df[['category', 'total']].groupby('category').sum(
).sort_values('total', ascending=False).round(0)

# %% [markdown]
# ## Reimbursement Calculations

# %%
date_cutoff = '3/1/22'

# %%
# importing required modules


# %%
aux = df.loc[df['date'] < date_cutoff]
print(aux['total'].sum())
display(aux)

# %%
aux = df.loc[df['date'] >= date_cutoff]
print(aux['total'].sum())
display(aux)
