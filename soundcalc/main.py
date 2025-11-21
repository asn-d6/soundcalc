from __future__ import annotations
import json

from soundcalc.common.utils import KIB
from soundcalc.regimes.best_attack import best_attack_security
from soundcalc.zkvms.fri_based_vm import get_DEEP_ALI_errors
from soundcalc.zkvms.risc0 import Risc0Preset
from soundcalc.zkvms.miden import MidenPreset
from soundcalc.zkvms.zisk import ZiskPreset
from soundcalc.regimes.johnson_bound import JohnsonBoundRegime
from soundcalc.regimes.unique_decoding import UniqueDecodingRegime
from soundcalc.report import build_markdown_report
from soundcalc.zkvms.zkvm import zkVM



def generate_and_save_md_report(sections) -> None:
    """
    Generate markdown report and save it to disk.
    """
    md = build_markdown_report(sections)
    md_path = "results.md"

    with open(md_path, "w", encoding="utf-8") as f:
        f.write(md)

    print(f"wrote :: {md_path}")


def print_summary_for_zkvm(zkvm: zkVM) -> None:
    """
    Print a summary of security results for a single zkVM.
    """
    print("")
    print("#############################################")
    print(f"#  zkVM: {zkvm.get_name()}")
    print("#############################################")
    proof_size_kib = zkvm.get_proof_size_bits() // KIB
    print("")
    print(f"proof size estimate: {proof_size_kib} KiB, where 1 KiB = 1024 bytes")
    print("")
    print(f"parameters: \n {zkvm.get_parameter_summary()}")
    print("")
    print(f"security levels (rbr): \n {json.dumps(zkvm.get_security_levels(), indent=4)}")
    print("")
    print("")
    print("")
    print("")

def main() -> None:
    """
    Main entry point for soundcalc

    Analyze multiple zkVMs across different security regimes,
    generate reports, and save results to disk.
    """

    # We consider the following zkVMs
    zkvms = [
        ZiskPreset.default(),
        MidenPreset.default(),
        Risc0Preset.default(),
    ]

    # Analyze each zkVM
    for zkvm in zkvms:
        print_summary_for_zkvm(zkvm)

    # Generate and save markdown report
    # TODO. re-integrate
    # generate_and_save_md_report(sections)

if __name__ == "__main__":
    main()
