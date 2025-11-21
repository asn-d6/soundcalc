"""This file is a mess"""

from __future__ import annotations

import math
from typing import Dict, Any, List, Tuple

from soundcalc.common.utils import KIB



def build_markdown_report(sections) -> str:

    lines: list[str] = []
    lines.append("# zkEVM soundcalc report")
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

        (zkvm_obj, results) = sections[zkevm]
        display_results: dict[str, Any] = {
            name: data.copy() if isinstance(data, dict) else data
            for name, data in results.items()
        }

        # Add parameter information
        lines.append(f"**Parameters:**")
        lines.append(f"- Number of queries: {zkvm_obj.num_queries}")
        lines.append(f"- Grinding (bits): {zkvm_obj.grinding_query_phase}")
        # Get field name from the field extension degree and base field
        field_name = "Unknown"
        if hasattr(zkvm_obj, 'field_extension_degree'):
            if zkvm_obj.field_extension_degree == 2:
                field_name = "Goldilocks²"
            elif zkvm_obj.field_extension_degree == 3:
                field_name = "Goldilocks³"
            elif zkvm_obj.field_extension_degree == 4:
                field_name = "BabyBear⁴"
            elif zkvm_obj.field_extension_degree == 5:
                field_name = "BabyBear⁵"
        lines.append(f"- Field: {field_name}")
        lines.append(f"- Rate (ρ): {zkvm_obj.rho}")
        lines.append(f"- Trace length (H): $2^{{{zkvm_obj.h}}}$")
        if zkvm_obj.power_batching:
            lines.append(f"- Batching: Powers")
        else:
            lines.append(f"- Batching: Affine")
        lines.append("")

        # Proof size
        proof_size_kib = zkvm_obj.get_proof_size_bits() // KIB
        lines.append(f"**Proof Size Estimate:** {proof_size_kib} KiB, where 1 KiB = 1024 bytes")
        lines.append("")

        # Show results

        # --- Get all column headers ---
        columns = set()
        for v in display_results.values():
            if isinstance(v, dict):
                columns.update(v.keys())

        ordered_columns: list[str] = ["regime"]
        if "total" in columns:
            ordered_columns.append("total")
        ordered_columns.extend(sorted(col for col in columns if col != "total"))
        columns = ordered_columns

        fri_commit_columns = [
            col for col in columns if col.startswith("FRI commit round ")
        ]

        def should_collapse_commit_columns() -> bool:
            if len(fri_commit_columns) <= 1:
                return False

            def row_has_single_value(row: dict[str, Any]) -> bool:
                values = [row.get(col) for col in fri_commit_columns if col in row]
                values = [value for value in values if value is not None]
                if not values:
                    return True
                first_value = values[0]
                return all(value == first_value for value in values)

            for row_data in display_results.values():
                if isinstance(row_data, dict) and not row_has_single_value(row_data):
                    return False
            return True

        if should_collapse_commit_columns():
            first_commit_idx = columns.index(fri_commit_columns[0])
            for col in fri_commit_columns:
                columns.remove(col)

            merged_label = f"FRI commit rounds (×{len(fri_commit_columns)})"
            columns.insert(first_commit_idx, merged_label)

            for row_name, row_data in display_results.items():
                if not isinstance(row_data, dict):
                    continue
                merged_value = None
                for col in fri_commit_columns:
                    if col in row_data:
                        merged_value = row_data[col]
                        break
                if merged_value is not None:
                    row_data[merged_label] = merged_value
                for col in fri_commit_columns:
                    row_data.pop(col, None)

        # --- Build Markdown header ---
        md_table = "| " + " | ".join(columns) + " |\n"
        md_table += "| " + " | ".join(["---"] * len(columns)) + " |\n"

        # --- Build each row ---
        for row_name, row_data in display_results.items():
            row_values = [row_name]
            if isinstance(row_data, dict):
                for col in columns[1:]:
                    row_values.append(str(row_data.get(col, "—")))
            else:
                # Non-dict value sits under the 'total' column when present.
                for col in columns[1:]:
                    if col == "total":
                        row_values.append(str(row_data))
                    else:
                        row_values.append("—")
            md_table += "| " + " | ".join(row_values) + " |\n"

        lines.append(md_table)


    return "\n".join(lines)
