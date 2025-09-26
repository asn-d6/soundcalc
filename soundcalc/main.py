from __future__ import annotations

import math
from soundcalc.zkevms.risc0 import Risc0Preset
from soundcalc.zkevms.miden import MidenPreset
from soundcalc.regimes.ethstark import ToyProblemRegime
from soundcalc.regimes.johnson_bound import JohnsonBoundRegime
from soundcalc.regimes.capacity_bound import CapacityBoundRegime
from soundcalc.regimes.unique_decoding import UniqueDecodingRegime
from soundcalc.report import build_combined_html_report, build_markdown_report
from .common.utils import KIB

def compute_security_for_zkevm(security_regimes: list, params) -> dict[str, dict]:
    """
    Compute bits of security for a single zkEVM across all security regimes.
    """
    results: dict[str, dict] = {}

    for security_regime in security_regimes:
        total_bits, details = security_regime.compute_security(params)
        results[security_regime.identifier()] = {
            "total_bits": total_bits,
            "details": dict(details),
        }

    return results


def generate_and_save_md_report(sections: list[tuple[str, dict[str, dict], object]]) -> None:
    """
    Generate markdown report and save it to disk.
    """
    md = build_markdown_report(title="soundcalc results", sections=sections)
    md_path = "results.md"

    with open(md_path, "w", encoding="utf-8") as f:
        f.write(md)

    print(f"wrote :: {md_path}")


def print_summary_for_zkevm(zkevm_params, security_regimes: list, results: dict[str, dict]) -> None:
    """
    Print a summary of security results for a single zkEVM.
    """
    totals_line = "; ".join([f"{name}: {res['total_bits']:.3f}b" for name, res in results.items()])
    print(f"zkEVM: {zkevm_params.name}")
    print(f"  proof size estimate: {zkevm_params.proof_size_bits / KIB} KiB, where 1 KiB = 2^10 Byte")
    print(f"  totals :: {totals_line}")

    # Print security for each security regime
    for security_regime in security_regimes:
        security_regime.print_security_summary()


def main() -> None:
    """
    Main entry point for soundcalc

    Analyze multiple zkEVMs across different security regimes,
    generate reports, and save results to disk.
    """
    # Data structure for compiling the markdown report
    sections: list[tuple[str, dict[str, dict], object]] = []

    zkevms = [
        Risc0Preset.default(),
        MidenPreset.default(),
    ]

    security_regimes = [
        UniqueDecodingRegime(),
        JohnsonBoundRegime(),
        CapacityBoundRegime(),
        ToyProblemRegime(),
    ]

    # Analyze each zkEVM across all security regimes
    for zkevm_params in zkevms:
        results = compute_security_for_zkevm(security_regimes, zkevm_params)
        print_summary_for_zkevm(zkevm_params, security_regimes, results)
        sections.append((zkevm_params.name, results, zkevm_params))

    # Generate and save markdown report
    generate_and_save_md_report(sections)

if __name__ == "__main__":
    main()
