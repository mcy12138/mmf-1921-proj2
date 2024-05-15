import cvxpy as cp
import numpy as np


def MVO(mu, Q):
    """
    #---------------------------------------------------------------------- Use this function to construct an example of a MVO portfolio.
    #
    # An example of an MVO implementation is given below. You can use this
    # version of MVO if you like, but feel free to modify this code as much
    # as you need to. You can also change the inputs and outputs to suit
    # your needs.

    # You may use quadprog, Gurobi, or any other optimizer you are familiar
    # with. Just be sure to include comments in your code.

    # *************** WRITE YOUR CODE HERE ***************
    #----------------------------------------------------------------------
    """

    # Find the total number of assets
    n = len(mu)

    # Set the target as the average expected return of all assets
    targetRet = np.mean(mu)

    # Disallow short sales
    lb = np.zeros(n)

    # Add the expected return constraint
    A = -1 * mu.T
    b = -1 * targetRet

    # constrain weights to sum to 1
    Aeq = np.ones([1, n])
    beq = 1
    A = A.to_numpy()

    # Define and solve using CVXPY
    x = cp.Variable(n)
    prob = cp.Problem(cp.Minimize((1 / 2) * cp.quad_form(x, Q)),
                      [A @ x <= b,
                       Aeq @ x == beq,
                       x >= lb])
    prob.solve(verbose=False)
    return x.value

def RP(Q):
    n = Q.shape[0]

    # Assign an arbitrary value for kappa
    kappa = 5

    # Define the optimization variable
    x = cp.Variable(n)

    # Objective function
    objective = 0.5 * cp.quad_form(x, Q) - kappa * cp.sum(cp.log(x))

    # Constraints
    constraints = [x >= 0, cp.sum(x) == 1]  # x >= 0 and sum(x) = 1

    # Define and solve the problem
    problem = cp.Problem(cp.Minimize(objective), constraints)
    problem.solve()

    # Recover the weights
    x_value = x.value

    # Calculate the individual risk contribution per asset
    RC = (x_value * (Q @ x_value)) / np.sqrt(np.dot(x_value.T, Q @ x_value))

    # Return the optimized portfolio and the associated cost
    return x.value



