"""
A few FRI-related utilities used across regimes.
"""

from __future__ import annotations

import math
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ..zkvms.zkvm import FRIBasedVM

def get_johnson_parameter_m() -> float:
    """
    Return m from https://eprint.iacr.org/2022/1216.pdf
    """
    # ASN This is hardcoded to 16, whereas winterfell brute forces it:
    #    https://github.com/facebook/winterfell/blob/main/air/src/proof/security.rs#L290-L306
    return 16.0

def get_num_FRI_folding_rounds(
    witness_size: int,
    field_extension_degree: int,
    folding_factor: int,
    fri_early_stop_degree: int,
) -> int:
    """
    Compute the number of FRI folding rounds.
    Stolen from:
      https://github.com/risc0/risc0/blob/release-2.0/risc0/zkp/src/prove/soundness.rs#L125
    """
    rounds = 0
    n = int(witness_size)
    while n // int(field_extension_degree) > int(fri_early_stop_degree):
        n //= int(folding_factor)
        rounds += 1
    return rounds

def get_FRI_query_phase_error(theta: float, num_queries: int, grinding_bits: int) -> float:
    """
    Compute the FRI query phase soundness error.
    See the last term of Equation 7 in Theorem 2 of Ha22.

    It includes `grinding_query_phase_bits` bits of grinding.

    Note: This function is used by all regimes except the toy problem regime (TPR).
    """
    FRI_query_phase_error = (1 - theta) ** num_queries

    # Add bits of security from grinding (see section 6.3 in ethSTARK)
    FRI_query_phase_error *= 2 ** (-grinding_bits)

    return FRI_query_phase_error

def get_size_of_merkle_path_bits(num_leafs: int, tuple_size: int, element_size_bits: int, hash_size_bits: int) -> int:
    """
    Compute the size of a Merkle path in bits.

    We assume a Merkle tree that represents num_leafs tuples of elements
    where each element has size element_size_bits and one tuple contains tuple_size
    many elements. Each leaf of the tree contains one such tuple.

    Note: the result counts both the leaf itself and the Merkle path.
    """
    assert num_leafs > 0
    leaf_size = tuple_size * element_size_bits
    sibling = tuple_size * element_size_bits
    tree_depth = math.ceil(math.log2(num_leafs))
    co_path = (tree_depth - 1) * hash_size_bits
    return leaf_size + sibling + co_path


def get_FRI_proof_size_bits(
        hash_size_bits: int,
        field_size_bits: int,
        num_functions: int,
        num_queries: int,
        witness_size: int,
        field_extension_degree: int,
        early_stop_degree: int,
        folding_factor: int,
) -> int:

    """
    Compute the proof size of a (BCS-transformed) FRI interaction in bits.
    """

    # TODO: the following things are not yet considered.
    #   - is there really a Merkle root (and paths) for the final round? Or just the codeword itself?

    # The FRI proof contains two parts: Merkle roots, and one "openings" per query,
    # where an "opening" is a Merkle path for each folding layer.
    #
    # We use the same loop as in `get_num_FRI_folding_rounds`, and count the size that
    # this layer contributes, which includes the root and all Merkle paths.

    size_bits = 0

    # Initial Round: one root and one path per query
    # We assume that for the initial functions, there is only one Merkle root, and
    # each leaf i for that root contains symbols i for all initial functions.
    n = int(witness_size)
    num_leafs = n // int(folding_factor)
    tuple_size = num_functions
    size_bits += hash_size_bits + num_queries * get_size_of_merkle_path_bits(num_leafs, tuple_size, field_size_bits, hash_size_bits)


    # Folding rounds
    # We assume that "siblings" for the following layers are grouped together
    # in one leaf. This is natural as they always need to be opened together.

    # TODO: need to check if that is actually the correct loop
    while n // int(folding_factor * field_extension_degree) >= int(early_stop_degree):
        n //= int(folding_factor)
        num_leafs = n // int(folding_factor)
        tuple_size = folding_factor
        # one root and one path per query
        size_bits += hash_size_bits + num_queries * get_size_of_merkle_path_bits(num_leafs, tuple_size, field_size_bits, hash_size_bits)

    return size_bits