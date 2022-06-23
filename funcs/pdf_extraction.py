import glob
from pathlib import Path
from typing import Union
from IPython.display import display


import PyPDF2
import pandas as pd


def _extract_pdf_text(file_path: str) -> Union[str, None]:
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


def _extract_total_frm_str(text: str) -> Union[float, None]:
    import re
    if text is None:
        return None
    text = text.title().replace('Subtotal', '').replace(
        'Sub Total', '').replace('(Incl.Tax)', '')
    text = text.replace('Food & Bev Total:', '')
    search = re.compile(
        r"(\(\$\d*\.\d*\)|Total( Payment)?:?\s*\$[\s]?\d*\.\d*)")
    sub_search = re.compile(r"\d*\.\d*")
    search_results = search.search(text)
    if search_results is None:
        return None
    pdf_total = float(sub_search.search(search_results.group()).group())
    return pdf_total


def _expand_wildcard_paths(root_paths):
    file_paths = []
    for root_path in root_paths:
        file_paths += glob.glob(f"{root_path}*.pdf") + \
            glob.glob(f"{root_path}*.PDF")

    return file_paths


def _set_unparsed_totals(df):
    print("**** Files with parsing errors ****")
    unparsed_pdfs_df = df.loc[df['total'].isnull()]
    display(unparsed_pdfs_df)

    print("**** Setting unparsed totals from filename ****")
    df.loc[df.index.isin(unparsed_pdfs_df.index), 'total'] = unparsed_pdfs_df['filename'].str.split(
        '.').str[0].str.split('$').str[1].str.replace('_', '.').astype('float')

    print("**** Files still without totals ****")
    display(df.loc[df['total'].isnull()])


def load_pdf_file_totals_to_df(file_paths):
    rows = []
    for file_path in _expand_wildcard_paths(file_paths):
        file_name = Path(file_path).name
        folder_name = Path(file_path).parent.name
        total = _extract_total_frm_str(_extract_pdf_text(file_path=file_path))
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

    _set_unparsed_totals(df)

    return df
