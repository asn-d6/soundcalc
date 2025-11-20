from __future__ import annotations

from .fri_regime import FRIParameters, FRIRegime
from typing import Any
from ..common.utils import get_rho_plus
from soundcalc.common.fri import (
    get_johnson_parameter_m,
    get_FRI_query_phase_error,
)
import math

class JohnsonBoundRegime(FRIRegime):
    """
    List decoding up-to-Johnson bound regime (JBR):
    The proximity parameter θ is in the range `(1 - ρ)/2 < θ < 1 - √ρ` where ρ is the rate

    This is Regime 2 from the RISC0 Python calculator
    """

    def identifier(self) -> str:
        return "JBR"

    def get_bound_on_list_size(self, params: FRIParameters) -> int:
        """
        Returns an upper bound on the list size of this regime, i.e., the number of codewords
        a function is close to.
        """

        # The value is from the Guruswami-Sudan decoder.
        # Concrete formulas and notation are taken from pages 16-18 of [Ha22] with
        # the final formula from Theorem 8 of [Ha22].
        m = self._get_m()
        alpha, theta = self._get_alpha_and_theta(params.rho, m)
        r_plus = get_rho_plus(params.trace_length, params.D, params.max_combo)
        # Sanity checks. The theta must have been selected to have this valid
        # TODO guarantee that
        assert theta < 1 - math.sqrt(r_plus)
        m_plus = self._get_minimal_m_plus(r_plus, alpha)
        assert theta <= 1 - math.sqrt(r_plus) * (1 + 1 / (2 * m_plus))

        # Note: Miden computes L differently (see eps_1 of Theorem 2 of https://eprint.iacr.org/2024/1553.pdf)
        # TODO figure out the right one for Miden
        #    L_miden = m / (params.rho - (2.0 * m / params.D));
        # Small difference for RISC0 parameters:
        #  RISC0=35, Miden=64
        return (m_plus + 0.5) / math.sqrt(r_plus)

    def get_theta(self, params: FRIParameters) -> float:
        """
        Returns the theta for the query phase error.
        """
        m = self._get_m()
        alpha, theta = self._get_alpha_and_theta(params.rho, m)
        return theta


    def get_batching_error(self, params: FRIParameters) -> float:
        """
        Returns the error for the FRI batching step for this regime.
        """

        # Note: the errors for correlated agreement in the following two cases differ,
        # which is related to the batching method:
        #
        # Case 1: we batch with randomness r^0, r^1, ..., r^{num_functions-1}
        # This is what is called batching over parameterized curves in BCIKS20.
        # Here, the error depends on num_functions (called l in BCIKS20), and we find
        # the error in Theorem 6.2.
        #
        # Case 2: we batch with randomness r_0 = 1, r_1, r_2, r_{num_functions-1}
        # This is what is called batching over affine spaces in BCIKS20.
        # Here, the error does not depend on num_functions (called l in BCIKS20), and we find
        # the error in Theorem 1.6.
        #
        # Then easiest way to see the difference is to compare Theorems 1.5 and 1.6.

        m = self._get_m()
        rho = params.rho
        error = ((m + 0.5) ** 5) / (3 * (rho ** 1.5)) * (params.D) / params.F
        if params.power_batching:
            error *= params.num_functions
        return error

    def get_commit_phase_error(self, params: FRIParameters) -> float:
        """
        Returns the error for the FRI commit phase for this regime.
        """

        # See Theorem 8.3 of BCIKS20.
        # Also, seen in Theorem 2 of Ha22, and Theorem 1 of eSTARK paper.

        # Note: This function is also used by CBR, but there is no good foundation for it yet.
        # TODO Find a better formula for CBR.

        # TODO: check this formula carefully
        m = self._get_m()
        error = (2 * m + 1) * (params.D + 1) * params.folding_factor / (math.sqrt(params.rho) * params.F)
        return error


    def _get_alpha_and_theta(self, rho: float, m: float) -> tuple[float, float]:
        """
        Compute alpha and theta. See Theorem 2 of Ha22.
        """
        # ASN Is this a good value for eta?

        # eta denotes our distance from the JB
        eta = math.sqrt(rho) / (2 * m)

        # Given the above eta, we have:
        #   alpha = sqrt(rho) * (1 + 1/(2m))
        # as required by Theorem 2 of Ha22.
        alpha = math.sqrt(rho) + eta

        # And proximity parameter theta = 1 - sqrt(rho) - eta
        #                               = 1 - sqrt(rho) * (1 + 1/ (2m) )
        # as required by Theorem 2 of Ha22.
        theta = 1 - alpha
        return alpha, theta

    def _get_minimal_m_plus(self, r_plus: float, alpha: float) -> int:
        # ASN RISC0 rust soundness also puts max_combo in here:
        #         let m_plus = 1.0 / (params.biggest_combo * (alpha / rho_plus.sqrt() - 1.0));
        return math.ceil(1 / (2 * (alpha / math.sqrt(r_plus) - 1)))

    def _get_m(self):
        m = get_johnson_parameter_m()  # TODO DK: it is not clear if this is the right m to use. To investigate.
        return m
