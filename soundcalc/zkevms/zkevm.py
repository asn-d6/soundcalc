from __future__ import annotations

from dataclasses import dataclass
from typing import Protocol, Mapping, Any

from math import log2
from ..common.fields import FieldParams
from ..common.fri import get_num_FRI_folding_rounds



@dataclass(frozen=True)
class zkEVMConfig:
    """
    A zkEVM configuration that should be provided by the user.
    """

    # Name of the proof system
    name: str

    # The code rate ρ
    rho: float
    # Domain size before low-degree extension (i.e. trace length)
    trace_length: int
    # Preset field parameters (contains p, ext_size, F)
    field: FieldParams
    # Total columns of AIR table
    num_columns: int
    # Number of polynomials appearing in the batched-FRI
    # This can be greater than `num_columns`: some zkEVMs have to use "segment polynomials" (aka "composition polynomials")
    num_polys: int
    # Number of FRI queries
    num_queries: int

    # FRI folding factor (arity of folding per round)
    FRI_folding_factor: int
    # Many zkEVMs don't FRI fold until the final poly is of degree 1. They instead stop earlier.
    # This is the degree they stop at (and it influences the number of FRI folding rounds).
    FRI_early_stop_degree: int

    # Maximum number of entries from a single column referenced in a single constraint
    max_combo: int

    # Proof of Work grinding compute during FRI query phase (expressed in bits of security)
    grinding_query_phase: int


class zkEVMParams:
    """
    zkEVM parameters used by the soundness calculator.
    """
    def __init__(self, zkevm_cfg: zkEVMConfig):
        """
        Given a zkEVMConfig, compute all the parameters relevant for the zkEVM.
        """
        # Copy the parameters over (also see docs just above)
        self.name = zkevm_cfg.name
        self.rho = zkevm_cfg.rho
        self.trace_length = zkevm_cfg.trace_length
        self.num_columns = zkevm_cfg.num_columns
        self.num_polys = zkevm_cfg.num_polys
        self.num_queries = zkevm_cfg.num_queries
        self.max_combo = zkevm_cfg.max_combo
        self.FRI_folding_factor = zkevm_cfg.FRI_folding_factor
        self.FRI_early_stop_degree = zkevm_cfg.FRI_early_stop_degree
        self.grinding_query_phase = zkevm_cfg.grinding_query_phase

        # Number of columns should be less or equal to the final number of polynomials in batched-FRI
        assert self.num_columns <= self.num_polys

        # Now, also compute some auxiliary parameters

        # Negative log of rate
        self.k = int(round(-log2(self.rho)))
        # Log of trace length
        self.h = int(round(log2(self.trace_length)))
        # Domain size, after low-degree extension
        self.D = self.trace_length / self.rho

        # Extract field parameters from the preset field
        # Extension field degree (e.g., ext_size = 2 for Fp²)
        self.field_extension_degree = zkevm_cfg.field.field_extension_degree
        # Extension field size |F| = p^{ext_size}
        self.F = zkevm_cfg.field.F

        # Compute number of FRI folding rounds
        self.FRI_rounds_n = get_num_FRI_folding_rounds(
            witness_size=int(self.D),
            field_extension_degree=int(self.field_extension_degree),
            folding_factor=int(self.FRI_folding_factor),
            fri_early_stop_degree=int(self.FRI_early_stop_degree),
        )

