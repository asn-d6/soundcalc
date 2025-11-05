from __future__ import annotations
import json

from soundcalc.common.utils import KIB, get_proof_system_levels
from soundcalc.regimes.best_attack import best_attack_security
from soundcalc.zkevms.risc0 import Risc0Preset
from soundcalc.zkevms.miden import MidenPreset
from soundcalc.zkevms.zisk import ZiskPreset
from soundcalc.regimes.johnson_bound import JohnsonBoundRegime
from soundcalc.regimes.capacity_bound import CapacityBoundRegime
from soundcalc.regimes.unique_decoding import UniqueDecodingRegime
from soundcalc.report import build_markdown_report


def get_rbr_levels_for_zkevm_and_regime(regime, params) -> dict[str, int]:

    # the round-by-round errors consist of the ones for FRI and for the proof system
    # and we also add a total, which is the minimum over all of them.

    fri_levels = regime.get_rbr_levels(params)
    list_size = regime.get_bound_on_list_size(params)

    proof_system_levels = get_proof_system_levels(list_size, params)

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


def print_summary_for_zkevm(zkevm_params, results: dict[str, dict]) -> None:
    """
    Print a summary of security results for a single zkEVM.
    """
    print(f"zkEVM: {zkevm_params.name}")
    proof_size_kib = zkevm_params.proof_size_bits // KIB
    print(f"    proof size estimate: {proof_size_kib} KiB, where 1 KiB = 1024 bytes")
    print(json.dumps(results, indent=4))
    print("")
    print("")


def main() -> None:
    """
    Main entry point for soundcalc

    Analyze multiple zkEVMs across different security regimes,
    generate reports, and save results to disk.
    """
    # Data structure for compiling the markdown report
    sections = {}

    zkevms = [
        Risc0Preset.default(),
        MidenPreset.default(),
        ZiskPreset.default(),
    ]

    security_regimes = [
        UniqueDecodingRegime(),
        JohnsonBoundRegime(),
        CapacityBoundRegime(),
    ]

    # Analyze each zkEVM across all security regimes
    for zkevm_params in zkevms:
        results = compute_security_for_zkevm(security_regimes, zkevm_params)
        print_summary_for_zkevm(zkevm_params, results)
        sections[zkevm_params.name] = (zkevm_params, results)

    # Generate and save markdown report
    generate_and_save_md_report(sections)

if __name__ == "__main__":
    main()
