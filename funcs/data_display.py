from IPython.display import display


def display_df_split_by_time(spend_df, date_cutoff):
    pre_cuttoff_df = spend_df.loc[spend_df['date'] < date_cutoff]
    print(f'Pre-{date_cutoff}')
    print(pre_cuttoff_df['total'].sum())
    display(pre_cuttoff_df)

    post_cuttoff_df = spend_df.loc[spend_df['date'] >= date_cutoff]
    print(f'Post-{date_cutoff}')
    print(post_cuttoff_df['total'].sum())
    display(post_cuttoff_df)


def display_totals(spend_df, income_df, str_carry_over_tag: str = 'CarryOver'):
    carry_over_mask = (income_df['sponsor'] == str_carry_over_tag)
    print('+ Total Income:\t\t %.2f' % income_df['amount'].sum())
    print('\t| New Income\t %.2f' % income_df.loc[~carry_over_mask]['amount'].sum())
    print('\t| Carry Over\t %.2f' % income_df.loc[carry_over_mask]['amount'].sum())
    print('- Total Spent:\t\t %.2f' % spend_df['total'].sum())
    print('===================')
    print('Remaining Balance:\t %.2f' % (income_df['amount'].sum()-spend_df['total'].sum()))
