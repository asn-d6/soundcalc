from __future__ import annotations

import math
from typing import Optional, Dict, Any

from ..zkevms.zkevm import zkEVMParams


class Regime:
    """
    A class representing a generic regime. Soundcalc supports four regimes:
    - Unique Decoding Regime (UDR)
    - List Decoding up to Johnson Bound (JBR),
    - List Decoding up to Capacity Bound (CBR).
    - Toy Problem Regime (TPR),
    Code for those regimes can be found in files across this directory.

    This class carries around the soundness errors and computes the final bits of security.

    Each of the errors below represent soundness errors for different parts of the proof system.
    They are tiny values (e.g. 2^-100) that represent the probability that the verifier, for every
    cheating prover, accepts a false proof.
    We convert it to "bits of security" by taking the negative log2 of the soundness error.
    """

    # This is the error from the proximity gaps (part of the FRI commit phase)
    e_proximity_gap: Optional[float] = None
    # This is the batched-FRI commit-phase soundness error
    # It is described in Theorem 2 of Ha22
    # it is also described in Theorem 1 of the eSTARK paper
    e_FRI_commit_phase: Optional[float] = None
    # This is the batched-FRI query-phase soundness error
    e_FRI_query_phase: Optional[float] = None
    # This is the final FRI soundness error
    e_FRI_final: Optional[float] = None

    # Soundness error for the rest of the proof system
    e_ALI: Optional[float] = None
    e_DEEP: Optional[float] = None
    e_PLONK: Optional[float] = None
    e_PLOOKUP: Optional[float] = None

    # This is the final soundness error for the entire proof system
    e_final: Optional[float] = None


    def identifier(self) -> str:
        raise NotImplementedError

    def compute_security(self, params: zkEVMParams) -> tuple[float, dict[str, Any]]:
        raise NotImplementedError

    def gets_bits_of_security_from_error(self) -> tuple[float, dict[str, Any]]:
        """Convert soundness error to bits of security"""
        # The errors below MUST be set at this point.
        # Whereas some other errors (e.g. e_proximity_gaps) might not be set in some regimes (e.g. TPR)
        assert self.e_final
        assert self.e_FRI_commit_phase
        assert self.e_FRI_query_phase
        assert self.e_FRI_final
        assert self.e_PLONK
        assert self.e_PLOOKUP
        # Assert for all other errors if we are not in the toy problem regime
        if self.identifier() != "toy_problem":
            assert self.e_proximity_gap
            assert self.e_ALI
            assert self.e_DEEP

        bits = -math.log2(self.e_final)
        details: Dict[str, Any] = {
            "e_proximity_gaps": self.e_proximity_gap,
            "e_FRI_constant": self.e_FRI_commit_phase,
            "e_FRI_queries": self.e_FRI_query_phase,
            "e_FRI_final": self.e_FRI_final,
            "e_final": self.e_final,
        }
        # Include granular proof-system components if available
        details["e_ALI"] = self.e_ALI
        details["e_DEEP"] = self.e_DEEP
        details["e_PLONK"] = self.e_PLONK
        details["e_PLOOKUP"] = self.e_PLOOKUP
        return (bits, details)

    def _print_bits_of_security_for_error(self, error: Optional[float], label: str) -> None:
        """Print error as bits of security if not None"""
        if error is not None:
            bits = -math.log2(error)
            print(f"    {label}: {bits:.1f}b")

    def print_security_summary(self) -> None:
        """
        Print a detailed security breakdown for this regime.
        Shows all error components as bits of security.
        """
        print(f"  {self.identifier()}:")

        # Print FRI-related errors as bits of security
        self._print_bits_of_security_for_error(self.e_proximity_gap, "proximity_gaps")
        self._print_bits_of_security_for_error(self.e_FRI_commit_phase, "FRI_constant")
        self._print_bits_of_security_for_error(self.e_FRI_query_phase, "FRI_queries")
        self._print_bits_of_security_for_error(self.e_FRI_final, "FRI_final")

        # Print proof system errors as bits of security
        self._print_bits_of_security_for_error(self.e_ALI, "ALI")
        self._print_bits_of_security_for_error(self.e_DEEP, "DEEP")
        self._print_bits_of_security_for_error(self.e_PLONK, "PLONK")
        self._print_bits_of_security_for_error(self.e_PLOOKUP, "PLOOKUP")
        self._print_bits_of_security_for_error(self.e_final, "final")

