from __future__ import annotations

from dataclasses import dataclass
from typing import Protocol, Mapping, Any

from math import log2

from soundcalc.common.utils import get_bits_of_security_from_error
from soundcalc.regimes.fri_regime import FRIParameters
from soundcalc.regimes.johnson_bound import JohnsonBoundRegime
from soundcalc.regimes.unique_decoding import UniqueDecodingRegime
from soundcalc.zkvms.zkvm import zkVM
from ..common.fields import FieldParams, field_element_size_bits
from ..common.fri import get_FRI_proof_size_bits, get_num_FRI_folding_rounds



def get_DEEP_ALI_errors(L_plus: float, params: FRIBasedVM):
    """
    Compute common proof system error components that are shared across regimes.
    Some of them depend on the list size L_plus

    Returns a dictionary containing levels for ALI and DEEP
    """

    # TODO Check that it holds for all regimes

    # XXX These proof system errors are actually quite RISC0 specific.
    # See Section 3.4 from the RISC0 technical report.
    # We might want to generalize this further for other zkEVMs.
    # For example, Miden also computes similar values for DEEP-ALI in:
    # https://github.com/facebook/winterfell/blob/2f78ee9bf667a561bdfcdfa68668d0f9b18b8315/air/src/proof/security.rs#L188-L210
    e_ALI = L_plus * params.num_columns / params.F
    e_DEEP = (
        L_plus
        * (params.AIR_max_degree * (params.trace_length + params.max_combo - 1) + (params.trace_length - 1))
        / (params.F - params.trace_length - params.D)
    )

    levels = {}
    levels["ALI"] = get_bits_of_security_from_error(e_ALI)
    levels["DEEP"] = get_bits_of_security_from_error(e_DEEP)

    return levels

@dataclass(frozen=True)
class FRIBasedVMConfig:
    """
    A configuration of a FRI-based zkVM
    """

    # Name of the proof system
    name: str

    # The output length of the hash function that is used in bits
    # Note: this concerns the hash function used for Merkle trees
    hash_size_bits: int

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
    # Boolean flag to indicate if batched-FRI is implemented using coefficients
    # r^0, r^1, ... r^{num_polys-1} (power_batching = True) or
    # 1, r_1, r_2, ... r_{num_polys - 1} (power_batching = False)
    power_batching: bool
    # Number of FRI queries
    num_queries: int
    # Maximum constraint degree
    AIR_max_degree: int

    # FRI folding factor (arity of folding per round)
    FRI_folding_factor: int
    # Many zkEVMs don't FRI fold until the final poly is of degree 1. They instead stop earlier.
    # This is the degree they stop at (and it influences the number of FRI folding rounds).
    FRI_early_stop_degree: int

    # Maximum number of entries from a single column referenced in a single constraint
    max_combo: int

    # Proof of Work grinding compute during FRI query phase (expressed in bits of security)
    grinding_query_phase: int


class FRIBasedVM(zkVM):
    """
    Models a zkVM that is based on FRI.
    """
    def __init__(self, config: FRIBasedVMConfig):
        """
        Given a config, compute all the parameters relevant for the zkVM.
        """
        # Copy the parameters over (also see docs just above)
        self.name = config.name
        self.hash_size_bits = config.hash_size_bits
        self.rho = config.rho
        self.trace_length = config.trace_length
        self.num_columns = config.num_columns
        self.num_polys = config.num_polys
        self.power_batching = config.power_batching
        self.num_queries = config.num_queries
        self.max_combo = config.max_combo
        self.FRI_folding_factor = config.FRI_folding_factor
        self.FRI_early_stop_degree = config.FRI_early_stop_degree
        self.grinding_query_phase = config.grinding_query_phase
        self.AIR_max_degree = config.AIR_max_degree

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
        self.field_extension_degree = config.field.field_extension_degree
        # Extension field size |F| = p^{ext_size}
        self.field = config.field
        self.F = config.field.F

        # Compute number of FRI folding rounds
        self.FRI_rounds_n = get_num_FRI_folding_rounds(
            witness_size=int(self.D),
            field_extension_degree=int(self.field_extension_degree),
            folding_factor=int(self.FRI_folding_factor),
            fri_early_stop_degree=int(self.FRI_early_stop_degree),
        )



    def get_name(self) -> str:
        return self.name

    def get_parameters(self) -> str:
        """
        Returns a description of the parameters of the zkVM.
        The description is given as a string.
        """
        # TODO: insert something here
        return ""

    def get_proof_size_bits(self) -> int:
        """
        Returns an estimate for the proof size, given in bits.
        """

        # Compute the proof size
        # XXX (BW): note that it is not clear that this is the
        # proof size for every zkEVM we can think of
        # XXX (BW): we should probably also add something for the OOD samples and plookup, lookup etc.

        return get_FRI_proof_size_bits(
            hash_size_bits=self.hash_size_bits,
            field_size_bits=field_element_size_bits(self.field),
            num_functions=self.num_queries,
            num_queries=self.num_queries,
            witness_size=int(self.D),
            field_extension_degree=int(self.field_extension_degree),
            early_stop_degree=int(self.FRI_early_stop_degree),
            folding_factor=int(self.FRI_folding_factor),
        )

    def get_security_levels(self) -> dict[str, dict[str, int]]:
        """
        Returns a dictionary that maps each regime (i.e., a way of doing security analysis)
        to a dictionary that contains the round-by-round soundness levels.

        It maps from a label that describes the regime (e.g., UDR, JBR in case of FRI) to a
        regime-specific dictionary. Any such regime-specific dictionary is as follows:

        It maps from a label that explains which round it is for to an integer.
        If this integer is, say, k, then it means the error for this round is at
        most 2^{-k}.
        """

        # we consider the following regimes, and for each regime do the analysis
        regimes = [
            UniqueDecodingRegime(),
            JohnsonBoundRegime(),
        ]

        fri_parameters = FRIParameters(
            hash_size_bits=self.hash_size_bits,
            field_size_bits=field_element_size_bits(self.field),
            rho=self.rho,
            num_functions=self.num_queries,
            num_queries=self.num_queries,
            witness_size=int(self.D),
            D=self.D,
            F=self.F,
            FRI_rounds_n=self.FRI_rounds_n,
            power_batching=self.power_batching,
            field_extension_degree=int(self.field_extension_degree),
            early_stop_degree=int(self.FRI_early_stop_degree),
            folding_factor=int(self.FRI_folding_factor),
            grinding_query_phase=self.grinding_query_phase,
            trace_length=self.trace_length,
            max_combo=self.max_combo
        )

        result = {}
        for regime in regimes:
            id = regime.identifier()

            # errors consist of FRI errors and proof system errors
            fri_levels = regime.get_rbr_levels(fri_parameters)
            list_size = regime.get_bound_on_list_size(fri_parameters)
            proof_system_levels = get_DEEP_ALI_errors(list_size, self)
            total = min(list(fri_levels.values()) + list(proof_system_levels.values()))

            result[id] = fri_levels | proof_system_levels | {"total": total}

        return result
