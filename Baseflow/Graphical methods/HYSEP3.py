# HYSEP3: Local Minimum Method
def local_minimum(Q, N):
    # Calculate half-window size k = (N - 1) / 2
    k = (N - 1) // 2  
    
    is_datetime = pd.api.types.is_datetime64_any_dtype(Q.index)
    
    # Identify local minima
    minima_days = []
    minima_values = []
    
    for t in Q.index:
        # Define the window: from t - k to t + k, adjusted for boundaries
        if is_datetime:
            start = max(Q.index[0], t - pd.Timedelta(days=k))
            end = min(Q.index[-1], t + pd.Timedelta(days=k))
        else:
            start = max(Q.index[0], t - k)
            end = min(Q.index[-1], t + k)
        
        window = Q.loc[start:end]
        min_idx = window.idxmin()
        
        # Check if current day t is the minimum in its window
        if min_idx == t and pd.notna(min_idx):
            minima_days.append(t)
            minima_values.append(Q[t])
    
    # If no minima are found, return a copy of the Q
    if not minima_days:
        return Q.copy()
    
    # Create baseflow series
    b = pd.Series(index=Q.index, dtype=float)
    
    # Linearly interpolate between minima
    for i in range(len(minima_days) - 1):
        t1, t2 = minima_days[i], minima_days[i + 1]
        b1, b2 = minima_values[i], minima_values[i + 1]
        
        # Convert indices to numeric for interpolation (days since start)
        if is_datetime:
            t1_num = (t1 - Q.index[0]).days
            t2_num = (t2 - Q.index[0]).days
            t_range = pd.date_range(t1, t2, freq='D')
            t_num = [(t - Q.index[0]).days for t in t_range]
        else:
            t1_num = t1
            t2_num = t2
            t_range = range(t1, t2 + 1)
            t_num = t_range
        
        # Interpolate baseflow values
        for t, t_n in zip(t_range, t_num):
            fraction = (t_n - t1_num) / (t2_num - t1_num)
            b[t] = b1 + (b2 - b1) * fraction
    
    # Handle days before the first minimum and after the last minimum
    if is_datetime:
        b.loc[b.index <= minima_days[0]] = minima_values[0]
        b.loc[b.index >= minima_days[-1]] = minima_values[-1]
    else:
        b.loc[:minima_days[0]] = minima_values[0]
        b.loc[minima_days[-1]:] = minima_values[-1]
    
    return b