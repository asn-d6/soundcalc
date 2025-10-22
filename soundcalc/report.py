"""This file is a mess"""

from __future__ import annotations

import math
from typing import Dict, Any, List, Tuple

from soundcalc.common.utils import KIB



def build_markdown_report(sections) -> str:

    lines: list[str] = []
    lines.append("#zkEVM soundcalc report")
    lines.append("")
    lines.append("Each row is a zkEVM proof system.\nEach column is a different component of the proof system.\nThe cell values are the bits of security for each such component.")
    lines.append("")

    # ToC
    lines.append("## zkEVMs")
    for zkevm in sections:
        anchor = zkevm.lower().replace(" ", "-")
        lines.append(f"- [{zkevm}](#{anchor})")
    lines.append("")

    for zkevm in sections:
        anchor = zkevm.lower().replace(" ", "-")
        lines.append(f"## {zkevm}")
        lines.append("")

        (zkevm_params, results) = sections[zkevm]

        # Add parameter information
        lines.append(f"**Parameters:**")
        lines.append(f"- Number of queries: {zkevm_params.num_queries}")
        lines.append(f"- Grinding (bits): {zkevm_params.grinding_query_phase}")
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
        if zkevm_params.power_batching:
            lines.append(f"- Batching: Powers")
        else:
            lines.append(f"- Batching: Affine")
        lines.append("")

        # Proof size
        proof_size_kib = zkevm_params.proof_size_bits // KIB
        lines.append(f"**Proof Size Estimate:** {proof_size_kib} KiB, where 1 KiB = 1024 bytes")
        lines.append("")

        # Show results

        # --- Get all column headers ---
        columns = set()
        for v in results.values():
            if isinstance(v, dict):
                columns.update(v.keys())
        columns = ["regime"] + sorted(columns)  # 'row' will be the first column

        # --- Build Markdown header ---
        md_table = "| " + " | ".join(columns) + " |\n"
        md_table += "| " + " | ".join(["---"] * len(columns)) + " |\n"

        # --- Build each row ---
        for row_name, row_data in results.items():
            row_values = [row_name]
            if isinstance(row_data, dict):
                for col in columns[1:]:
                    row_values.append(str(row_data.get(col, "—")))
            else:
                # Non-dict value (e.g. 'ethstark toy problem')
                row_values +=  ["—"] * (len(columns) - 2) + [str(row_data)]
            md_table += "| " + " | ".join(row_values) + " |\n"

        lines.append(md_table)


    return "\n".join(lines)
