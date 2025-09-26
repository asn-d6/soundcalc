# soundcalc results

Each row is a zkEVM proof system.
Each column is a different component of the proof system.
The cell values are the bits of security for each such component.

## zkEVMs
- [risc0](#risc0)
- [miden](#miden)

## risc0

**Parameters:**
- Number of queries: 50
- Grinding (bits): 0
- Field: BabyBear⁴
- Rate (ρ): 0.25
- Trace length (H): 2^21
- Batching: Powers

<b>Proof Size Estimate:</b> 250.83984375 KiB, where 1 KiB = 2^10 Byte

Regime | Final | Proximity_gaps | FRI_commit | FRI_query | FRI_final | ALI | DEEP | PLONK | PLOOKUP
--- | --- | --- | --- | --- | --- | --- | --- | --- | ---
UDR | 33 | 92 | 92 | **33** | 33 | 115 | 100 | 98 | 96
JBR | 31 | 39 | **31** | 47 | 31 | 110 | 95 | 98 | 96
CBR | 72 | 86 | 78 | 86 | 78 | 88 | **72** | 98 | 96
TPR | 96 | — | 123 | 100 | 99 | — | — | 98 | **96**

## miden

**Parameters:**
- Number of queries: 27
- Grinding (bits): 16
- Field: Goldilocks²
- Rate (ρ): 0.125
- Trace length (H): 2^18
- Batching: Powers

<b>Proof Size Estimate:</b> 120.90625 KiB, where 1 KiB = 2^10 Byte

Regime | Final | Proximity_gaps | FRI_commit | FRI_query | FRI_final | ALI | DEEP | PLONK | PLOOKUP
--- | --- | --- | --- | --- | --- | --- | --- | --- | ---
UDR | 38 | 100 | 100 | **38** | 38 | 121 | 106 | 106 | 105
JBR | 41 | 48 | **41** | 55 | 41 | 115 | 101 | 106 | 105
CBR | 81 | 93 | 86 | 83 | 83 | 96 | **81** | 106 | 105
TPR | 96 | — | 127 | **97** | 96 | — | — | 106 | 105
