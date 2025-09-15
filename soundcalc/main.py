from __future__ import annotations

from soundcalc.zkevms.risc0 import Risc0Preset
from soundcalc.zkevms.miden import MidenPreset
from soundcalc.regimes.ethstark import EthStarkRegime
from soundcalc.regimes.johnson_bound import JohnsonBoundRegime
from soundcalc.regimes.capacity_bound import CapacityBoundRegime
from soundcalc.regimes.unique_decoding import UniqueDecodingRegime
from soundcalc.report import build_combined_html_report, build_markdown_report

def main() -> None:
    presets = [
        Risc0Preset.default(),
        MidenPreset.default(),
    ]

    regimes = [
        UniqueDecodingRegime(),
        JohnsonBoundRegime(),
        CapacityBoundRegime(),
        EthStarkRegime(),
    ]

    sections: list[tuple[str, dict[str, dict], object]] = []
    for params in presets:
        results: dict[str, dict] = {}
        for regime in regimes:
            total_bits, details = regime.estimate(params)
            results[regime.identifier()] = {
                "total_bits": total_bits,
                "details": dict(details),
            }
        totals_line = "; ".join([f"{name}: {res['total_bits']:.3f}b" for name, res in results.items()])
        print(f"zkEVM: {params.name}")
        print(f"  totals :: {totals_line}")
        sections.append((params.name, results, params))

    md = build_markdown_report(title="soundcalc results", sections=sections)
    md_path = "results.md"
    with open(md_path, "w", encoding="utf-8") as f:
        f.write(md)
    print(f"wrote :: {md_path}")

if __name__ == "__main__":
    main()


