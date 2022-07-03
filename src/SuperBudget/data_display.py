from IPython.display import display
from pandas import DataFrame


def display_df_split_by_time(df_spend: DataFrame, date_cutoff: str) -> None:
    df_pre_cuttoff = df_spend.loc[df_spend['date'] < date_cutoff]
    print(f'Pre {date_cutoff}')
    print('Total:', df_pre_cuttoff['total'].sum())
    display(df_pre_cuttoff)

    post_cuttoff_df = df_spend.loc[df_spend['date'] >= date_cutoff]
    print(f'Post {date_cutoff}')
    print('Total:', post_cuttoff_df['total'].sum())
    display(post_cuttoff_df)


def display_totals(df_spend: DataFrame, df_income: DataFrame, str_carry_over_tag: str = 'CarryOver') -> None:
    mask_carry_over = (df_income['sponsor'] == str_carry_over_tag)
    print('+ Total Income:\t\t %.2f' % df_income['amount'].sum())
    print('\t| New Income\t %.2f' % df_income.loc[~mask_carry_over]['amount'].sum())
    print('\t| Carry Over\t %.2f' % df_income.loc[mask_carry_over]['amount'].sum())
    print('- Total Spent:\t\t %.2f' % df_spend['total'].sum())
    print('===================')
    print('Remaining Balance:\t %.2f' % (df_income['amount'].sum()-df_spend['total'].sum()))
