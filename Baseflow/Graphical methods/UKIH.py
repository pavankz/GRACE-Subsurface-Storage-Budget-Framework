# Revised United Kingdom Insitute of Hydrology (UKIH) method
def revised_ukih(Q, block_size=5):
    N = len(Q)
    df_bf = pd.DataFrame(index=Q.index)
    
    for s in range(block_size):
        # Initialize with Q's datetime index
        assigned_bf_s = pd.Series(index=Q.index, dtype=float)
        t = s
        while t <= N - block_size:
            d = t + (block_size - 1) // 2  # Middle day of the block
            if d < N:
                b = Q.iloc[t:t+block_size].min()
                assigned_bf_s.iloc[d] = b  # Assign to position d, which maps to Q.index[d]
            t += block_size
        
        # Interpolate between assigned points
        bf_s = assigned_bf_s.interpolate(method='linear')
        
        # Fill before first assigned date and after last assigned date
        first_assigned_date = assigned_bf_s.first_valid_index()
        last_assigned_date = assigned_bf_s.last_valid_index()
        if first_assigned_date is not None:
            bf_s.loc[bf_s.index < first_assigned_date] = assigned_bf_s[first_assigned_date]
        if last_assigned_date is not None:
            bf_s.loc[bf_s.index > last_assigned_date] = assigned_bf_s[last_assigned_date]
        
        df_bf[f's{s}'] = bf_s
    
    # Compute median across all starting points
    b_final = df_bf.median(axis=1)
    
    # Ensure baseflow does not exceed Q
    b_final = b_final.clip(upper=Q)
    
    return b_final
