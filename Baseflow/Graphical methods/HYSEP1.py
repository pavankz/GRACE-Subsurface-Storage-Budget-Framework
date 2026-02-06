# HYSEP1: Fixed Interval method
def fixed_interval(Q, N):

    b = pd.Series(index=Q.index, dtype=float)
    total_days = len(Q)
    
    # Iterate over the time series in steps of 'interval(N)' days
    for start in range(0, total_days, N):
        end = min(start + N, total_days)
        interval_data = Q.iloc[start:end]
        min_discharge = interval_data.min()  # Find the lowest discharge in the interval
        b.iloc[start:end] = min_discharge  # Assign it to all days in the interval
    
    return b