#######################################################################
# Function definition automatically generated by solver_diagnostics.py
#
# Use the function defined here to generate and run the best
# smoothed aggregation method found by solver_diagnostics(...).
# The only argument taken is a CSR/BSR matrix.
#
# To run:  >>> # User must load/generate CSR/BSR matrix A
#          >>> from solver_diagnostic import solver_diagnostic
#          >>> solver_diagnostic(A)
#######################################################################

from pyamg import smoothed_aggregation_solver
from pyamg.util.linalg import norm
from numpy import ones, array, arange, zeros, abs, random
from scipy import rand, ravel, log10, kron, eye
from scipy.io import loadmat
from scipy.sparse import isspmatrix_bsr, isspmatrix_csr
import pylab

def solver_diagnostic(A):
    ##
    # Generate B
    B = ones((A.shape[0],1), dtype=A.dtype); BH = B.copy()

    ##
    # Random initial guess, zero right-hand side
    random.seed(0)
    b = zeros((A.shape[0],1))
    x0 = rand(A.shape[0],1)

    ##
    # Create solver
    ml = smoothed_aggregation_solver(A, B=B, BH=BH,
        strength=('symmetric', {'theta': 0.0}),
        smooth=('energy', {'weighting': 'local', 'krylov': 'gmres', 'degree': 1, 'maxiter': 2}),
        improve_candidates=[('gauss_seidel_nr', {'sweep': 'symmetric', 'iterations': 4}), None],
        aggregate="standard",
        presmoother=('gauss_seidel_nr', {'sweep': 'symmetric', 'iterations': 2}),
        postsmoother=('gauss_seidel_nr', {'sweep': 'symmetric', 'iterations': 2}),
        max_levels=15,
        max_coarse=300,
        coarse_solver="pinv")

    ##
    # Solve system
    res = []
    x = ml.solve(b, x0=x0, tol=1e-08, residuals=res, accel="gmres", maxiter=300, cycle="V")
    res_rate = (res[-1]/res[0])**(1.0/(len(res)-1.))
    normr0 = norm(ravel(b) - ravel(A*x0))
    print " "
    print ml
    print "System size:                " + str(A.shape)
    print "Avg. Resid Reduction:       %1.2f"%res_rate
    print "Iterations:                 %d"%len(res)
    print "Operator Complexity:        %1.2f"%ml.operator_complexity()
    print "Work per DOA:               %1.2f"%(ml.cycle_complexity()/abs(log10(res_rate)))
    print "Relative residual norm:     %1.2e"%(norm(ravel(b) - ravel(A*x))/normr0)

    ##
    # Plot residual history
    pylab.semilogy(array(res)/normr0)
    pylab.title('Residual Histories')
    pylab.xlabel('Iteration')
    pylab.ylabel('Relative Residual Norm')
    pylab.show()

