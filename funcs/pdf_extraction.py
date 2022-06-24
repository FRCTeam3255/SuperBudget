import glob
from pathlib import Path
from typing import Collection, Union
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


def _expand_wildcard_paths(root_paths: Collection) -> Collection:
    file_paths = []
    for root_path in root_paths:
        file_paths += glob.glob(f"{root_path}*.pdf") + \
            glob.glob(f"{root_path}*.PDF")

    return file_paths


def _set_unparsed_totals(df: pd.DataFrame) -> None:
    print("**** Files with parsing errors ****")
    unparsed_pdfs_df = df.loc[df['total'].isnull()]
    display(unparsed_pdfs_df)

    print("**** Setting unparsed totals from filename ****")
    df.loc[df.index.isin(unparsed_pdfs_df.index), 'total'] = unparsed_pdfs_df['filename'].str.split(
        '.').str[0].str.split('$').str[1].str.replace('_', '.').astype('float')
    df.loc[df.index.isin(unparsed_pdfs_df.index), 'total_source'] = 'file_name'
    df.loc[~df.index.isin(unparsed_pdfs_df.index), 'total_source'] = 'file_parsing'

    print("**** Files still without totals ****")
    display(df.loc[df['total'].isnull()])


def get_pdf_totals(file_paths: Union[str, Collection], print_paths: bool = False) -> pd.DataFrame:
    if isinstance(file_paths, str) and ('.csv' in file_paths):
        # Read in file paths (ignoring # comments found in file)
        file_paths = pd.read_csv(
            'file_paths.csv',
            comment='#',  # comment
            index_col=0,
            header=None,
        ).index.to_list()
    elif isinstance(file_paths, list):
        pass  # NOSONAR # Disables linting check on line
    else:
        raise TypeError('file_paths should be a .csv filename or python list of filepaths')
    rows = []
    if print_paths:
        print('File paths to be used')
        print(_expand_wildcard_paths(file_paths))
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
