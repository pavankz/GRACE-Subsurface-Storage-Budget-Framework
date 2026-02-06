# HYSEP2: Sliding Interval method

def sliding_interval(Q, N):

    k = (N - 1) // 2     
    b = pd.Series(index=Q.index, dtype=float)
    
    # Check if index is datetime or integer
    is_datetime = pd.api.types.is_datetime64_any_dtype(Q.index)
    
    for t in Q.index:

        if is_datetime:
            start = max(Q.index[0], t - pd.Timedelta(days=k))
            end = min(Q.index[-1], t + pd.Timedelta(days=k))

        else:
            start = max(Q.index[0], t - k)
            end = min(Q.index[-1], t + k)
        
        # Select the window and assign the minimum discharge
        window = Q.loc[start:end]
        b[t] = window.min()
    
    return b