# Exponentially moving Weighted Average Filter
def EWMA(Q, b_LH, a, e, return_exceed=False):
    """exponential weighted moving average (EWMA) filter (Tularam & Ilahee, 2008)
        Q : streamflow
        e : smoothing parameter
    """
    if return_exceed:
        b = np.zeros(Q.shape[0] + 1)
    else:
        b = np.zeros(Q.shape[0])
    b[0] = b_LH[0]
    for i in range(Q.shape[0] - 1):
        b[i + 1] = (1 - e) * b[i] + e * Q[i + 1]
        if b[i + 1] > Q[i + 1]:
            b[i + 1] = Q[i + 1]
            if return_exceed:
                b[-1] += 1
    return b