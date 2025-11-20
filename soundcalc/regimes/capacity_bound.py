from __future__ import annotations

import math

# TODO: Conjectured.
C1 = 1.0
C2 = 1.0
C3 = 1.0 # List size related

from .fri_regime import FRIParameters, FRIRegime
from soundcalc.common.fri import get_johnson_parameter_m
from ..common.utils import get_rho_plus

class CapacityBoundRegime(FRIRegime):
    """
    List decoding up to Capacity Bound Regime (CBR)

    This is Regime 3 from the RISC0 python calculator.
    This regime assumes the proximity conjecture with parameters C1,C2 + the list size
    conjecture parameter C3.
    """

    def identifier(self) -> str:
        return "CBR"


    def get_bound_on_list_size(self, params: FRIParameters) -> int:
        """
        Returns an upper bound on the list size of this regime, i.e., the number of codewords
        a function is close to.
        """

        # ASN This computation is again kinda different between Ha22 and STIR conjecture.
        # Clarify and document why we are using this one.
        r_plus = get_rho_plus(params.trace_length, params.D, params.max_combo)
        # we assume that the theta has been chosen that this assert always holds
        # however, we might want to guarantee that
        # TODO DK: figure out how to guarantee that
        theta = self.get_theta(params)
        assert theta < 1 - r_plus
        eta_plus = 1 - r_plus - theta

        return math.ceil((params.D / eta_plus) ** C3)


    def get_theta(self, params: FRIParameters) -> float:
        """
        Returns the theta for the query phase error.
        """
        eta = self._get_eta()
        theta = 1 - params.rho - eta
        return theta


    def get_batching_error(self, params: FRIParameters) -> float:
        """
        Returns the error for the FRI batching step for this regime.
        """

        eta = self._get_eta()
        rho = params.rho

        # Note: the errors for correlated agreement in the following two cases differ,
        # which is related to the batching method:
        #
        # Case 1: we batch with randomness r^0, r^1, ..., r^{num_functions-1}
        # This is what is called batching over parameterized curves in BCIKS20.
        # Here, the error depends on num_functions (called l in BCIKS20), and we find
        # the error in Conjecture 8.4, second item.
        #
        # Case 2: we batch with randomness r_0 = 1, r_1, r_2, r_{num_functions-1}
        # This is what is called batching over affine spaces in BCIKS20.
        # Here, the error does not depend on num_functions (called l in BCIKS20), and we find
        # the error in Conjecture 8.4, first item.
        #
        # Then easiest way to see the difference is to compare Theorems 1.5 and 1.6.
        term_one =  1 / ((eta * rho) ** C1)
        term_two =  (params.D ** C2) / params.F
        error = term_one * term_two
        if params.power_batching:
            error *= params.num_functions ** C2
        return error

    def get_commit_phase_error(self, params: FRIParameters) -> float:
        """
        Returns the error for the FRI commit phase for this regime.
        """
        # Note: This function is used by CBR, but there is no good foundation for it yet.
        # It is just copied from JBR.
        # TODO Find a better formula for CBR.
        m = self._get_m()
        error = (2 * m + 1) * (params.D + 1) * params.folding_factor / (math.sqrt(params.rho) * params.F)
        return error


    def _get_eta(self):
        # This is called epsilon in the RISC0 calculator, but it's usually eta elsewhere
        # It denotes how close we are to the capacity bound
        # TODO DK: figure out if we can optimize this parameter
        eta = 0.05

        return eta

    def _get_m(self):
        m = get_johnson_parameter_m()  # TODO DK: it is not clear if this is the right m to use. To investigate.
        return m
