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
- Field: BabyBear⁴
- Rate (ρ): 0.25
- Trace length (H): 2^21

Regime | Final | Proximity_gaps | FRI_commit | FRI_query | FRI_final | ALI | DEEP | PLONK | PLOOKUP
--- | --- | --- | --- | --- | --- | --- | --- | --- | ---
UDR | 33 | 92 | 92 | **33** | 33 | 115 | 100 | 98 | 96
JB | 39 | 47 | **39** | 47 | 39 | 110 | 95 | 98 | 96
CBR | 72 | 86 | 78 | 86 | 78 | 88 | **72** | 98 | 96
ethSTARK | 96 | — | 123 | 100 | 99 | — | — | 98 | **96**

## miden

**Parameters:**
- Number of queries: 119
- Field: Goldilocks²
- Rate (ρ): 0.25
- Trace length (H): 2^18

Regime | Final | Proximity_gaps | FRI_commit | FRI_query | FRI_final | ALI | DEEP | PLONK | PLOOKUP
--- | --- | --- | --- | --- | --- | --- | --- | --- | ---
UDR | 100 | 106 | 104 | **100** | 100 | 121 | 107 | 106 | 105
JB | 57 | 58 | **57** | 133 | 57 | 116 | 102 | 106 | 105
CBR | 83 | 100 | 97 | 226 | 97 | 97 | **83** | 106 | 105
ethSTARK | 104 | — | 127 | 238 | 127 | — | — | 106 | **105**
