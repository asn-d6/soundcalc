

class zkVM:
    """
    A class modeling a zkVM.
    """

    def get_name(self) -> str:
        """
        Returns the name of the zkVM.
        """
        raise NotImplementedError

    def get_parameters(self) -> str:
        """
        Returns a description of the parameters of the zkVM.
        The description is given as a string.
        """
        raise NotImplementedError

    def get_proof_size_bits(self) -> int:
        """
        Returns an estimate for the proof size, given in bits.
        """
        raise NotImplementedError

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
        raise NotImplementedError
