from __future__ import annotations


from .fri_regime import FRIParameters, FRIRegime


class UniqueDecodingRegime(FRIRegime):
    """
    Unique decoding regime (UDR)

    This is Regime 4 from the RISC0 Python calculator

    Many thanks to the UDR-specific analysis of Paul Gafni and Al Kindi:
        https://hackmd.io/@pgaf/HkKs_1ytT
    """

    def identifier(self) -> str:
        return "UDR"

    def get_bound_on_list_size(self, params: FRIParameters) -> int:
        # For unique decoding, list size is naturally 1
        return 1

    def get_theta(self, params: FRIParameters) -> float:
        """
        Returns the theta for the query phase error.
        """
        theta = (1 - params.rho) / 2
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
        # the error in Theorem 6.1 and Theorem 1.5.
        #
        # Case 2: we batch with randomness r_0 = 1, r_1, r_2, r_{num_functions-1}
        # This is what is called batching over affine spaces in BCIKS20.
        # Here, the error does not depend on num_functions (called l in BCIKS20), and we find
        # the error in Theorem 1.6.
        #
        # Then easiest way to see the difference is to compare Theorems 1.5 and 1.6.

        error = params.D / params.F
        if params.power_batching:
            error *= params.num_functions
        return error

    def get_commit_phase_error(self, params: FRIParameters) -> float:
        """
        Returns the error for the FRI commit phase for this regime.
        """
        D = params.D
        FRI_folding_factor = params.folding_factor
        F = params.F

        fri_folding_error = (D * (FRI_folding_factor - 1)) / F
        return fri_folding_error
