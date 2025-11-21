
from dataclasses import dataclass

from soundcalc.common.fields import FieldParams
from soundcalc.zkvms.zkvm import zkVM

@dataclass(frozen=True)
class WHIRBasedVMConfig:
    """
    A configuration of a FRI-based zkVM
    """

    # Name of the proof system
    name: str

    # The output length of the hash function that is used in bits
    # Note: this concerns the hash function used for Merkle trees
    hash_size_bits: int

    # Parameters are inspired by Giacomo's script here for inspiration
    # https://github.com/WizardOfMenlo/stir-whir-scripts/blob/main/src/whir.rs

    # log2(1/rate), e.g., 2 if rate is 1/4
    # note that this is the rate of the initial code
    log_inv_rate: int

    # this is the number of WHIR iterations
    # note that a WHIR iteration consists of multiple rounds
    # this is denoted by M in the paper
    num_iterations: int

    # this is what is called k_0,...,k_{M-1} in the paper
    # as in Giacomo's script, we assume that this is the same for all
    # see https://github.com/WizardOfMenlo/stir-whir-scripts/blob/main/src/whir.rs#L72
    # in each iteration, we go from dimension 2^m_i to dimension 2^(m_i - k)
    folding_factor: int

    # the field that is used
    field: FieldParams

    # the log2 of the degree that we test
    # in the WHIR paper, this is denoted by m
    log_degree: int

    # how many functions do we test in one go
    # TODO (BW): need to check how batching is done in WHIR
    # batch_size: int

    # degree of constraints being proven on the committed words
    # This is d in Construction 5.1 in WHIR.
    constraint_degree: int

    # TODO (BW): grinding?
    # TODO: number of queries (different for each round)

    # the number of queries for each round (length M-1)
    num_queries: list[int]

    # the number of OOD samples for each round (length M-1)
    num_ood_samples: list[int]



class WHIRBasedVM(zkVM):
    """
    Models a zkVM that is based on WHIR.
    """
    def __init__(self, config: WHIRBasedVMConfig):
        """
        Given a config, compute all the parameters relevant for the zkVM.
        """
        self.name = config.name

        self.hash_size_bits = config.hash_size_bits
        self.folding_factor = config.folding_factor
        self.num_iterations = config.num_iterations
        self.field = config.field
        self.constraint_degree = config.constraint_degree
        self.num_queries = config.num_queries
        self.num_ood_samples = config.num_ood_samples

        # determine all rates (in contrast to FRI, these change over the iterations)
        # this also involves determining all log degrees
        assert(config.log_inv_rate > 0 and config.folding_factor >= 1)

        # the log degrees that we have are (m0, m1 = m0 - k, m2 = m0 - 2k, ..., m(M-1) = m0 - (M-1)k)
        assert (self.num_iterations * self.folding_factor <= config.log_degree)
        self.log_degrees = [config.log_degree - i * self.folding_factor for i in range(self.num_iterations)]

        # the eval domain sizes shrink by a factor of two, so the rates decrease by a factor of
        self.log_eval_domains = config.log_inv_rate + config.log_inv_rate
        self.log_inv_rates = [config.log_inv_rate + i * (self.folding_factor - 1) for i in range(self.num_iterations)]

        # ensure that we did not mess up with the number of rounds
        assert(len(self.num_ood_samples) == self.num_iterations - 1)
        assert(len(self.num_queries)     == self.num_iterations - 1)
        assert(len(self.log_degrees)     == self.num_iterations)
        assert(len(self.log_inv_rates)   == self.num_iterations)


    def get_name(self) -> str:
        return self.name

    def get_parameter_summary(self) -> str:
        lines = []
        lines.append("")
        lines.append("```")

        # Collect scalar parameters
        params = {
            "name": self.name,
            "hash_size_bits": self.hash_size_bits,
            "folding_factor": self.folding_factor,
            "num_iterations": self.num_iterations,
            "constraint_degree": self.constraint_degree,
            "field": self.field.to_string(),
        }

        key_width = max(len(k) for k in params)

        for k, v in params.items():
            lines.append(f"  {k:<{key_width}} : {v}")

        lines.append("")
        lines.append("  Per-round parameters:")
        lines.append(f"    log_degrees     : {self.log_degrees}")
        lines.append(f"    log_inv_rates   : {self.log_inv_rates}")
        lines.append(f"    num_queries     : {self.num_queries}")
        lines.append(f"    num_ood_samples : {self.num_ood_samples}")

        lines.append("```")
        return "\n".join(lines)

    def get_proof_size_bits(self) -> int:
        return -1 # TODO: implement

    def get_security_levels(self) -> dict[str, dict[str, int]]:
        return {} # TODO: implement