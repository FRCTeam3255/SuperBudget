# %% [markdown]
# # Setup

# %%
from typing import Union
import glob
from pathlib import Path
import pandas as pd
from pprint import pprint
import PyPDF2

# %%
# importing required modules


# %%
# Define functions
def extract_pdf_text(file_path: str) -> Union[str, None]:
    file_pdf = open(file_path, 'rb')

    # creating a pdf reader object
    reader_pdf = PyPDF2.PdfFileReader(file_pdf)

    # printing number of pages in pdf file
    full_pdf_text = ""
    try:
        for page in reader_pdf.pages:
            full_pdf_text += page.extractText()
    except Exception:
        return None

    file_pdf.close()
    full_pdf_text = full_pdf_text.replace(
        "!", "$").replace("\n", " ").replace(",", "")
    return full_pdf_text


def extract_total_frm_str(text: str) -> Union[float, None]:
    import re
    if text is None:
        return None
    text = text.title().replace('Subtotal', '').replace(
        'Sub Total', '').replace('(Incl.Tax)', '')
    text = text.replace('Food & Bev Total:', '')
    search = re.compile(
        r"(\(\$\d*\.\d*\)|Total( Payment)?[:]?\s*\$[\s]?\d*\.\d*)")
    sub_search = re.compile(r"\d*\.\d*")
    search_results = search.search(text)
    if search_results is None:
        return None
    pdf_total = float(sub_search.search(search_results.group()).group())
    return pdf_total


def get_pdf_total(file_path: str) -> str:
    return extract_total_frm_str(extract_pdf_text(file_path=file_path))


# %% [markdown]
# # Configuration

# %%
root_paths = [
    "/Users/Tayler/Documents/Robotics/Documents/2022 Specific/Receipts/",
    "/Users/Tayler/Documents/Robotics/Documents/2022 Specific/Receipts/Submitted/*/",
    "/Users/Tayler/Documents/Robotics/Documents/2022 Specific/Receipts/Submitted/",
    # "/Users/Tayler/Documents/Robotics/Documents/2022 Specific/Receipts/Physical Receipts/",
    # "/Users/Tayler/Documents/Robotics/Documents/2022 Specific/Receipts/Sykora Receipts/",
    # "/Users/Tayler/Documents/Robotics/Documents/2022 Specific/Receipts/PAID/"
]


# %% [markdown]
# # Run

# %%


file_paths = []
for root_path in root_paths:
    file_paths += glob.glob(f"{root_path}*.pdf") + \
        glob.glob(f"{root_path}*.PDF")
# file_paths

# %%
rows = []
for file_path in file_paths:
    file_name = Path(file_path).name
    folder_name = Path(file_path).parent.name
    total = get_pdf_total(file_path=file_path)
    rows.append({
        'total': total,
        'date': file_name.split()[0].replace('_', '-'),
        'vendor': file_name.split()[1],
        'filename': file_name,
        'folder': folder_name
    })
df = pd.DataFrame.from_records(rows)
df['date'] = pd.to_datetime(df['date'])
df = df.sort_values(['date', 'vendor'])
df = df.reset_index(drop=True)
df.to_csv('Total Costs.csv')


# %% [markdown]
# ## Validation Outputs

# %%
df.sort_values('total', ascending=False)  # .to_csv('items.csv')

# %%
print("**** Files with parsing errors ****")
try:
    unparsed_pdfs_df
except NameError:
    unparsed_pdfs_df = df.loc[df['total'].isnull()]
unparsed_pdfs_df

# %%
print("**** Setting unparsed totals from filename ****")
df.loc[df.index.isin(unparsed_pdfs_df.index), 'total'] = unparsed_pdfs_df['filename'].str.split(
    '.').str[0].str.split('$').str[1].str.replace('_', '.').astype('float')
print("**** Files without totals ****")
df.loc[df['total'].isnull()]


# %%
#
# for unparsed_pdf in unparsed_pdfs_df['filename'].items():
# 	# print(unparsed_pdf[1])
# 	file_name = unparsed_pdf[1]
# 	print("*"*5, file_name, "*"*5)
# file_name = '2021_12_14 CTRE Order 100007478.pdf'
# text = extract_pdf_text(file_path=root_path+file_name)
# print(text)


# def extract_total_frm_str2(text: str) -> float:
# 	import re
# 	search = re.compile(r"Total( Payment)?[:]?\s*\$[\s]?\d*\.\d*")
# 	sub_search = re.compile(r"\d*\.\d*")
# 	search_results = search.search(text.title())
# 	if search_results is None:
# 		return None
# 	pdf_total = float(sub_search.search(search_results.group()).group())
# 	return pdf_total

# extract_total_frm_str2(text)

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
aux

# %%
aux = df.loc[df['date'] >= date_cutoff]
print(aux['total'].sum())
aux
