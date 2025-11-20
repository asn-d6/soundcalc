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


def get_rbr_levels_for_zkevm_and_regime(regime, params) -> dict[str, int]:

    # the round-by-round errors consist of the ones for FRI and for the proof system
    # and we also add a total, which is the minimum over all of them.

    fri_levels = regime.get_rbr_levels(params)
    list_size = regime.get_bound_on_list_size(params)

    proof_system_levels = get_DEEP_ALI_errors(list_size, params)

    total = min(list(fri_levels.values()) + list(proof_system_levels.values()))

    return fri_levels | proof_system_levels | {"total": total}



def compute_security_for_zkevm(fri_regimes: list, params) -> dict[str, dict]:
    """
    Compute bits of security for a single zkEVM across all security regimes.
    """
    results: dict[str, dict] = {}

    # first all reasonable regimes
    for fri_regime in fri_regimes:
        rbr_errors = get_rbr_levels_for_zkevm_and_regime(fri_regime, params)
        results[fri_regime.identifier()] = rbr_errors

    # now the security based on the best known attack - for reference
    results["best attack"] = best_attack_security(params)

    return results


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
    print(f"zkVM: {zkvm.get_name()}")
    proof_size_kib = zkvm.get_proof_size_bits() // KIB
    print("")
    print(f"    proof size estimate: {proof_size_kib} KiB, where 1 KiB = 1024 bytes")
    print("")
    print(f"    parameters: \n {zkvm.get_parameters()}")
    print("")
    print(f"    security levels (rbr): \n {json.dumps(zkvm.get_security_levels(), indent=4)}")
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
