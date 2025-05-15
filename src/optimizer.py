import pandas as pd
import numpy as np
import cvxpy as cp

def optimize_portfolio(returns, signals):
    """Optimize portfolio weights using CVXPY for dollar-neutral positions."""
    weights = pd.DataFrame(index=returns.index, columns=returns.columns)
    for t in range(len(returns)):
        if signals[t] != 0:
            ret_t = returns.iloc[t].values
            cov_matrix = np.cov(returns.iloc[max(0, t-21):t].T)
            w = cp.Variable(2)
            risk = cp.quad_form(w, cov_matrix)
            expected_return = ret_t @ w
            constraints = [cp.sum(w) == 0, cp.norm(w, 1) <= 1]
            objective = cp.Minimize(risk - expected_return)
            prob = cp.Problem(objective, constraints)
            try:
                prob.solve()
                weights.iloc[t] = w.value if prob.status == cp.OPTIMAL else [0, 0]
            except Exception as e:
                print(f"Optimization failed at step {t}: {e}")
                weights.iloc[t] = [0, 0]
        else:
            weights.iloc[t] = [0, 0]
    return weights