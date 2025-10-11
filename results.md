#zkEVM soundcalc report

Each row is a zkEVM proof system.
Each column is a different component of the proof system.
The cell values are the bits of security for each such component.

## zkEVMs
- [risc0](#risc0)
- [miden](#miden)
- [ZisK](#zisk)

## risc0

**Parameters:**
- Number of queries: 50
- Grinding (bits): 0
- Field: BabyBear⁴
- Rate (ρ): 0.25
- Trace length (H): 2^21
- Batching: Powers

| regime | ALI | DEEP | FRI batching round | FRI commit round 1 | FRI commit round 2 | FRI commit round 3 | FRI commit round 4 | FRI query phase | PLONK | PLOOKUP | total |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| unique_decoding | 115 | 100 | 92 | 96 | 96 | 96 | 96 | 33 | 98 | 96 | 33 |
| johnson_bound | 110 | 95 | 39 | 90 | 90 | 90 | 90 | 47 | 98 | 96 | 39 |
| capacity_bound | 88 | 72 | 86 | 90 | 90 | 90 | 90 | 86 | 98 | 96 | 72 |
| ethstark toy problem | — | — | — | — | — | — | — | — | — | — | 95 |

## miden

**Parameters:**
- Number of queries: 27
- Grinding (bits): 16
- Field: Goldilocks²
- Rate (ρ): 0.125
- Trace length (H): 2^18
- Batching: Powers

| regime | ALI | DEEP | FRI batching round | FRI commit round 1 | FRI commit round 2 | FRI commit round 3 | FRI commit round 4 | FRI commit round 5 | FRI commit round 6 | FRI commit round 7 | FRI query phase | PLONK | PLOOKUP | total |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| unique_decoding | 121 | 106 | 100 | 105 | 105 | 105 | 105 | 105 | 105 | 105 | 38 | 106 | 105 | 38 |
| johnson_bound | 115 | 101 | 48 | 98 | 98 | 98 | 98 | 98 | 98 | 98 | 55 | 106 | 105 | 48 |
| capacity_bound | 96 | 81 | 93 | 98 | 98 | 98 | 98 | 98 | 98 | 98 | 83 | 106 | 105 | 81 |
| ethstark toy problem | — | — | — | — | — | — | — | — | — | — | — | — | — | 96 |

## ZisK

**Parameters:**
- Number of queries: 128
- Grinding (bits): 0
- Field: Unknown
- Rate (ρ): 0.5
- Trace length (H): 2^22
- Batching: Powers

| regime | ALI | DEEP | FRI batching round | FRI commit round 1 | FRI commit round 2 | FRI commit round 3 | FRI commit round 4 | FRI commit round 5 | FRI query phase | PLONK | PLOOKUP | total |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| unique_decoding | 185 | 167 | 162 | 165 | 165 | 165 | 165 | 165 | 53 | 166 | 164 | 53 |
| johnson_bound | 181 | 163 | 111 | 159 | 159 | 159 | 159 | 159 | 58 | 166 | 164 | 58 |
| capacity_bound | 158 | 140 | 157 | 159 | 159 | 159 | 159 | 159 | 110 | 166 | 164 | 110 |
| ethstark toy problem | — | — | — | — | — | — | — | — | — | — | — | 127 |
