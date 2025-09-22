"""This file is a mess"""

from __future__ import annotations

import math
from typing import Dict, Any, List, Tuple


def bits(x: float) -> float:
    return -math.log2(x)


def build_html_report(
    title: str,
    zk_name: str,
    results: Dict[str, Dict[str, Any]],
) -> str:
    # Requested row order with separators
    ORDER = [
        "e_final",
        "__SEP__",
        "e_FRI_final",
        "e_FRI_queries",
        "e_FRI_constant",
        "e_FRI_proximity_gaps",
        "__SEP__",
        "e_ALI",
        "e_DEEP",
        "e_PLONK",
        "e_PLOOKUP",
        "__SEP__",
        "e_arguments",
    ]

    # HTML head
    html: list[str] = []
    html.append("<!DOCTYPE html>")
    html.append("<html><head><meta charset='utf-8'>")
    html.append(f"<title>{title}</title>")
    html.append("<style>body{font-family:Inter,Arial,sans-serif;margin:20px;}h1{font-size:20px;}h2{font-size:16px;margin-top:22px;}table{border-collapse:collapse;width:100%;max-width:900px;}th,td{border:1px solid #ddd;padding:6px 8px;text-align:right}th:first-child,td:first-child{text-align:left}tr:nth-child(even){background:#fafafa}tr.sep td{border-top:2px solid #222;background:#fff}code{background:#f6f8fa;padding:1px 4px;border-radius:3px}</style>")
    html.append("</head><body>")
    html.append(f"<h1>{zk_name} — Regime Comparison</h1>")

    # Totals row
    html.append("<h2>Totals (-log2 P[err])</h2>")
    html.append("<table><thead><tr><th>Regime</th><th>Total Bits</th></tr></thead><tbody>")
    for regime, res in results.items():
        total_bits = res.get("total_bits")
        if isinstance(total_bits, (int, float)):
            html.append(f"<tr><td>{regime}</td><td>{math.floor(total_bits)}</td></tr>")
    html.append("</tbody></table>")

    # Per-error comparison table
    html.append("<h2>Error Term Comparison (-log2 P[err])</h2>")
    # Header
    regimes = list(results.keys())
    html.append("<table><thead><tr><th>Error Term</th>")
    for regime in regimes:
        html.append(f"<th>{regime}</th>")
    html.append("</tr></thead><tbody>")

    for key in ORDER:
        if key == "__SEP__":
            # separator row spanning all columns
            html.append(f"<tr class='sep'><td colspan='{1 + len(regimes)}'>&nbsp;</td></tr>")
            continue
        row_vals = []
        for regime in regimes:
            # allow alias: e_FRI_proximity_gaps <= e_proximity_gaps
            details = results[regime].get("details", {})
            val = details.get(key)
            if val is None and key == "e_FRI_proximity_gaps":
                val = details.get("e_proximity_gaps")
            if isinstance(val, (int, float)) and val > 0:
                row_vals.append(bits(val))
            else:
                row_vals.append(None)
        if any(v is not None for v in row_vals):
            html.append(f"<tr><td>{key}</td>")
            for v in row_vals:
                if v is None:
                    html.append("<td>—</td>")
                else:
                    html.append(f"<td>{math.floor(v)}</td>")
            html.append("</tr>")

    html.append("</tbody></table>")

    html.append("</body></html>")
    return "".join(html)


def build_combined_html_report(
    title: str,
    sections: List[Tuple[str, Dict[str, Dict[str, Any]], Any]],  # Added zkEVM params
) -> str:
    # Regime display order and mapping from identifiers to labels
    regime_order = [
        "unique_decoding",  # UDR
        "johnson_bound",    # JB
        "capacity_bound",   # CBR
        "ethstark",         # ethSTARK
    ]
    regime_label = {
        "unique_decoding": "UDR",
        "johnson_bound": "JB",
        "capacity_bound": "CBR",
        "ethstark": "ethSTARK",
    }

    # Column order and mapping to detail keys
    columns = [
        ("final", "e_final"),
        ("proximity_gaps", "e_proximity_gaps"),
        ("FRI_commit", "e_FRI_constant"),
        ("FRI_query", "e_FRI_queries"),
        ("FRI_final", "e_FRI_final"),
        ("ALI", "e_ALI"),
        ("DEEP", "e_DEEP"),
        ("PLONK", "e_PLONK"),
        ("PLOOKUP", "e_PLOOKUP"),
    ]

    html: list[str] = []
    html.append("<!DOCTYPE html>")
    html.append("<html><head><meta charset='utf-8'>")
    html.append(f"<title>{title}</title>")
    html.append("<style>body{font-family:Inter,Arial,sans-serif;margin:20px;}h1{font-size:22px;}h2{font-size:18px;margin-top:28px;}table{border-collapse:collapse;width:100%;max-width:1100px;}th,td{border:1px solid #ddd;padding:6px 8px;text-align:right}th:first-child,td:first-child{text-align:left}tr:nth-child(even){background:#fafafa}code{background:#f6f8fa;padding:1px 4px;border-radius:3px}.toc a{margin-right:12px}.hi{background:#ffd6d6}</style>")
    html.append("</head><body>")
    html.append(f"<h1>{title}</h1>")

    # Table of contents
    html.append("<div class='toc'><strong>zkEVMs:</strong> ")
    for zk_name, _, _ in sections:
        anchor = zk_name.replace(" ", "-")
        html.append(f"<a href='#sec-{anchor}'>{zk_name}</a>")
    html.append("</div>")

    # For each zkEVM, render a single table with regimes as rows and errors as columns
    for zk_name, results, zkevm_params in sections:
        anchor = zk_name.replace(" ", "-")
        html.append(f"<h2 id='sec-{anchor}'>{zk_name}</h2>")

        # Add parameter information
        field_name = "Unknown"
        if hasattr(zkevm_params, 'field_extension_degree'):
            if zkevm_params.field_extension_degree == 2:
                field_name = "Goldilocks²"
            elif zkevm_params.field_extension_degree == 4:
                field_name = "BabyBear⁴"

        html.append("<div style='margin-bottom: 16px;'>")
        html.append(f"<strong>Parameters:</strong><br>")
        html.append(f"• Number of queries: {zkevm_params.num_queries}<br>")
        html.append(f"• Field: {field_name}<br>")
        html.append(f"• Rate (ρ): {zkevm_params.rho}<br>")
        html.append(f"• Trace length (H): 2<sup>{zkevm_params.h}</sup>")
        html.append("</div>")

        # Header
        html.append("<table><thead><tr>")
        html.append("<th>Regime</th>")
        for col_name, _ in columns:
            html.append(f"<th>{col_name}</th>")
        html.append("</tr></thead><tbody>")

        # Rows in the specified regime order; skip if missing
        for regime_key in regime_order:
            if regime_key not in results:
                continue
            regime_res = results[regime_key]
            details = regime_res.get("details", {})

            # Gather bit values per column
            values_bits: List[Any] = []
            for _, detail_key in columns:
                val = details.get(detail_key)
                if isinstance(val, (int, float)) and val > 0:
                    values_bits.append(bits(val))
                else:
                    values_bits.append(None)

            # Determine which non-e_final and non-e_FRI_final cell is closest (in bits) to e_final
            final_bits = values_bits[0]
            fri_final_idx = next((i for i, (name, _) in enumerate(columns) if name == "FRI_final"), None)
            highlight_idx = None
            if isinstance(final_bits, (int, float)):
                best_diff = None
                for idx in range(1, len(values_bits)):
                    if fri_final_idx is not None and idx == fri_final_idx:
                        continue
                    v = values_bits[idx]
                    if isinstance(v, (int, float)):
                        diff = abs(v - final_bits)
                        if best_diff is None or diff < best_diff:
                            best_diff = diff
                            highlight_idx = idx

            # Render row
            html.append(f"<tr><td>{regime_label.get(regime_key, regime_key)}</td>")
            for idx, v in enumerate(values_bits):
                cls = " class=\"hi\"" if highlight_idx is not None and idx == highlight_idx else ""
                if isinstance(v, (int, float)):
                    html.append(f"<td{cls}>{math.floor(v)}</td>")
                else:
                    html.append(f"<td{cls}>—</td>")
            html.append("</tr>")

        html.append("</tbody></table>")

    html.append("</body></html>")
    return "".join(html)


def build_markdown_report(
    title: str,
    sections: List[Tuple[str, Dict[str, Dict[str, Any]], Any]],  # Added zkEVM params
) -> str:
    regime_order = [
        "unique_decoding",
        "johnson_bound",
        "capacity_bound",
        "ethstark",
    ]
    regime_label = {
        "unique_decoding": "UDR",
        "johnson_bound": "JB",
        "capacity_bound": "CBR",
        "ethstark": "ethSTARK",
    }
    columns = [
        ("Final", "e_final"),
        ("Proximity_gaps", "e_proximity_gaps"),
        ("FRI_commit", "e_FRI_constant"),
        ("FRI_query", "e_FRI_queries"),
        ("FRI_final", "e_FRI_final"),
        ("ALI", "e_ALI"),
        ("DEEP", "e_DEEP"),
        ("PLONK", "e_PLONK"),
        ("PLOOKUP", "e_PLOOKUP"),
    ]

    lines: list[str] = []
    lines.append(f"# {title}")
    lines.append("")
    lines.append("Each row is a zkEVM proof system.\nEach column is a different component of the proof system.\nThe cell values are the bits of security for each such component.")
    lines.append("")
    # TOC
    lines.append("## zkEVMs")
    for zk_name, _, _ in sections:
        anchor = zk_name.lower().replace(" ", "-")
        lines.append(f"- [{zk_name}](#{anchor})")
    lines.append("")

    for zk_name, results, zkevm_params in sections:
        anchor = zk_name.lower().replace(" ", "-")
        lines.append(f"## {zk_name}")
        lines.append("")

        # Add parameter information
        lines.append(f"**Parameters:**")
        lines.append(f"- Number of queries: {zkevm_params.num_queries}")
        # Get field name from the field extension degree and base field
        field_name = "Unknown"
        if hasattr(zkevm_params, 'field_extension_degree'):
            if zkevm_params.field_extension_degree == 2:
                field_name = "Goldilocks²"
            elif zkevm_params.field_extension_degree == 4:
                field_name = "BabyBear⁴"
        lines.append(f"- Field: {field_name}")
        lines.append(f"- Rate (ρ): {zkevm_params.rho}")
        lines.append(f"- Trace length (H): 2^{zkevm_params.h}")
        lines.append("")

        # Header row
        header = ["Regime"] + [name for name, _ in columns]
        sep = ["---"] * len(header)
        lines.append(" | ".join(header))
        lines.append(" | ".join(sep))

        for regime_key in regime_order:
            if regime_key not in results:
                continue
            details = results[regime_key].get("details", {})
            values_bits: List[Any] = []
            for _, detail_key in columns:
                val = details.get(detail_key)
                if isinstance(val, (int, float)) and val > 0:
                    values_bits.append(bits(val))
                else:
                    values_bits.append(None)

            # choose closest excluding e_final and e_FRI_final
            final_bits = values_bits[0]
            fri_final_idx = next((i for i, (name, _) in enumerate(columns) if name == "FRI_final"), None)
            highlight_idx = None
            if isinstance(final_bits, (int, float)):
                best_diff = None
                for idx in range(1, len(values_bits)):
                    if fri_final_idx is not None and idx == fri_final_idx:
                        continue
                    v = values_bits[idx]
                    if isinstance(v, (int, float)):
                        diff = abs(v - final_bits)
                        if best_diff is None or diff < best_diff:
                            best_diff = diff
                            highlight_idx = idx

            row: list[str] = [regime_label.get(regime_key, regime_key)]
            for idx, v in enumerate(values_bits):
                if isinstance(v, (int, float)):
                    cell = f"{math.floor(v)}"
                else:
                    cell = "—"
                if highlight_idx is not None and idx == highlight_idx:
                    cell = f"**{cell}**"
                row.append(cell)
            lines.append(" | ".join(row))
        lines.append("")

    return "\n".join(lines)
