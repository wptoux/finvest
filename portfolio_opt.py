import numpy as np
import scipy.optimize as sco
import math

__all__ = [
    'efficient_frontier'
]

def efficient_frontier(returns):
    '''
    '''
    n = returns.shape[1]
    noa = returns.shape[0]
    
    N = 100
    qs = [10**(5.0 * t/N - 1.0) for t in range(N)]
    
    Sigma = np.cov(returns)
    RT = np.mean(returns,axis=1)
    
    cons = ({'type':'eq','fun':lambda x:np.sum(x)-1})
    bnds = tuple((0,1) for x in range(noa))
    
    rets = []
    risks = []
    weights = []
    
    def markowitz_loss(weights,q):
        wT = weights.flatten()
        w = wT.T
        loss = wT.dot(Sigma).dot(w) - q * RT.dot(w)
        return loss
        
    for q in qs:
        res = sco.minimize(markowitz_loss, noa*[1./noa,], method='SLSQP', bounds=bnds, constraints=cons, args=(q))
        rets.append(RT.dot(res.x.T))
        risks.append(math.sqrt(res.x.T.dot(Sigma).dot(res.x)))
        weights.append(res.x)
        
    rets = np.array(rets)
    risks = np.array(risks)
    return rets,risks,weights