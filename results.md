# zkEVM soundcalc report

Each row is a zkEVM proof system.
Each column is a different component of the proof system.
The cell values are the bits of security for each such component.

## zkEVMs
- [ZisK](#zisk)
- [miden](#miden)
- [risc0](#risc0)

## ZisK

**Parameters:**
- Number of queries: 128
- Grinding (bits): 0
- Field: Goldilocks³
- Rate (ρ): 0.5
- Trace length (H): $2^{22}$
- Batching: Powers

**Proof Size Estimate:** 1352 KiB, where 1 KiB = 1024 bytes

| regime | total | ALI | DEEP | FRI batching round | FRI commit round 1 | FRI commit round 2 | FRI commit round 3 | FRI commit round 4 | FRI commit round 5 | FRI query phase |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| UDR | 53 | 185 | 167 | 162 | 165 | 165 | 165 | 165 | 165 | 53 |
| JBR | 58 | 181 | 163 | 111 | 159 | 159 | 159 | 159 | 159 | 58 |
| best attack | 128 | — | — | — | — | — | — | — | — | — |

## miden

**Parameters:**
- Number of queries: 27
- Grinding (bits): 16
- Field: Goldilocks²
- Rate (ρ): 0.125
- Trace length (H): $2^{18}$
- Batching: Powers

**Proof Size Estimate:** 114 KiB, where 1 KiB = 1024 bytes

| regime | total | ALI | DEEP | FRI batching round | FRI commit round 1 | FRI commit round 2 | FRI commit round 3 | FRI commit round 4 | FRI commit round 5 | FRI commit round 6 | FRI commit round 7 | FRI query phase |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| UDR | 38 | 121 | 106 | 100 | 105 | 105 | 105 | 105 | 105 | 105 | 105 | 38 |
| JBR | 48 | 115 | 101 | 48 | 98 | 98 | 98 | 98 | 98 | 98 | 98 | 55 |
| best attack | 96 | — | — | — | — | — | — | — | — | — | — | — |

## risc0

**Parameters:**
- Number of queries: 50
- Grinding (bits): 0
- Field: BabyBear⁴
- Rate (ρ): 0.25
- Trace length (H): $2^{21}$
- Batching: Powers

**Proof Size Estimate:** 223 KiB, where 1 KiB = 1024 bytes

| regime | total | ALI | DEEP | FRI batching round | FRI commit round 1 | FRI commit round 2 | FRI commit round 3 | FRI commit round 4 | FRI query phase |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| UDR | 33 | 115 | 100 | 92 | 96 | 96 | 96 | 96 | 33 |
| JBR | 39 | 110 | 95 | 39 | 90 | 90 | 90 | 90 | 47 |
| best attack | 99 | — | — | — | — | — | — | — | — |
