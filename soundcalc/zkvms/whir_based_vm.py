
from dataclasses import dataclass

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

    # TODO: add parameters, see Giacomo's script here for inspiration
    # https://github.com/WizardOfMenlo/stir-whir-scripts/blob/main/src/whir.rs



class WHIRBasedVM(zkVM):
    """
    Models a zkVM that is based on WHIR.
    """
    def __init__(self, config: WHIRBasedVMConfig):
        """
        Given a config, compute all the parameters relevant for the zkVM.
        """
        self.name = config.name
        pass

    def get_name(self) -> str:
        return self.name

    def get_parameters(self) -> str:
        raise NotImplementedError

    def get_proof_size_bits(self) -> int:
        raise NotImplementedError

    def get_security_levels(self) -> dict[str, dict[str, int]]:
        raise NotImplementedError