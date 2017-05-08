import pandas as pd


# Generated features:
# The method does not drop duplicates based on (pid, day)
# i.e. if a pid appears multiple times in a day, all the instances are kept
# and they will all have the same "daily" features
# itemsPurchased - revenue / price (for a single instance from that day)
# dailyRevenueMean - sum(revenue) / (count of pid occurence in thay day)
# dailyOccurencesCount - number of occurence of a pid in a day
# dailyTotalRevenue - total revenue for a pid, for a day
# dailyTotalItemsPurchased - sum(itemsPurchased) for a pid, for a day
def extract_daily_features(df):
    grouped = df.groupby(['pid', 'day'])
    df['itemsPurchased'] = df['revenue'] / df['price']
    grouped = grouped.agg({'revenue': ['mean', 'count', 'sum'], 'itemsPurchased': 'sum'})
    grouped.reset_index()
    grouped.reset_index(level=0, inplace=True)
    grouped.reset_index(level=0, inplace=True)
    grouped.columns = [' '.join(col).strip() for col in grouped.columns.values]
    joined = pd.merge(df, grouped, on=['pid', 'day'])
    joined.rename(columns={'revenue mean': 'dailyRevenueMean', 'revenue count': 'dailyOccurencesCount',
                           'revenue sum': 'dailyTotalRevenue', 'itemsPurchased sum': 'dailyTotalItemsPurchased'},
                  inplace=True)
    return joined

# Added featured:
# dailyOccurence - the index of the occurence in a specific day of a pid
# eg. pid 312 appears twice in day 2
# => the first occurence will have the feat. set to 0
# => the second occurence will have the feat. set to 1
def extract_daily_occurence(df):
    df.sort_values(by=['pid', 'day', 'lineID'], inplace=True)
    df['dailyOccurence'] = 0
    matrix = df.as_matrix(columns=['pid', 'day', 'dailyOccurence'])

    prev_day = 0
    prev_pid = 0
    current_occurence = 0

    for i in range(len(matrix)):
        if matrix[i, 0] != prev_pid or matrix[i, 1] != prev_day:
            if matrix[i, 0] % 1000 == 0:
                print
                matrix[i, 0]
            current_occurence = 0
        matrix[i, 2] = current_occurence
        current_occurence += 1
        prev_pid = matrix[i, 0]
        prev_day = matrix[i, 1]
    df.loc[:, 'dailyOccurence'] = matrix[:, 2]
    return df