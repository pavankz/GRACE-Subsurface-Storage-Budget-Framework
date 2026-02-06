# Low Flow Filter (Box car filter)
def LFF(Q):
    # Compute smoothed discharge
    smooth = pd.Series(index=Q.index)
    for t in Q.index:
        start = max(Q.index.min(), t - pd.Timedelta(days=15))
        end = min(Q.index.max(), t + pd.Timedelta(days=14))
        window = Q.loc[start:end]
        smooth[t] = window.mean()
    
    # Compute bias correction factor
    D = max(0, (smooth - Q).max())
    
    # Compute baseflow
    # b = smooth - D
    b = np.minimum(smooth, Q)
    # b = np.maximum(b, 0)
    return b