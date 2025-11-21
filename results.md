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

**Proof Size Estimate:** 992 KiB, where 1 KiB = 1024 bytes

| regime | total | ALI | DEEP | FRI batching round | FRI commit rounds (×5) | FRI query phase |
| --- | --- | --- | --- | --- | --- | --- |
| UDR | 53 | 185 | 167 | 162 | 165 | 53 |
| JBR | 58 | 181 | 163 | 142 | 159 | 58 |
| best attack | 128 | — | — | — | — | — |

## miden

**Parameters:**
- Number of queries: 27
- Grinding (bits): 16
- Field: Goldilocks²
- Rate (ρ): 0.125
- Trace length (H): $2^{18}$
- Batching: Powers

**Proof Size Estimate:** 175 KiB, where 1 KiB = 1024 bytes

| regime | total | ALI | DEEP | FRI batching round | FRI commit rounds (×7) | FRI query phase |
| --- | --- | --- | --- | --- | --- | --- |
| UDR | 38 | 121 | 106 | 100 | 105 | 38 |
| JBR | 55 | 115 | 101 | 77 | 98 | 55 |
| best attack | 96 | — | — | — | — | — |

## risc0

**Parameters:**
- Number of queries: 50
- Grinding (bits): 0
- Field: BabyBear⁴
- Rate (ρ): 0.25
- Trace length (H): $2^{21}$
- Batching: Powers

**Proof Size Estimate:** 576 KiB, where 1 KiB = 1024 bytes

| regime | total | ALI | DEEP | FRI batching round | FRI commit rounds (×4) | FRI query phase |
| --- | --- | --- | --- | --- | --- | --- |
| UDR | 33 | 115 | 100 | 92 | 96 | 33 |
| JBR | 47 | 110 | 95 | 70 | 90 | 47 |
| best attack | 99 | — | — | — | — | — |
