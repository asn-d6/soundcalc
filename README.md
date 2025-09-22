# soundcalc

🚧 **Really really WIP right now. Please give us some time.** 🚧

A universal soundness calculator across FRI-based zkEVM proof systems and security regimes.

It aims to answer questions like:
- "What if RISC0 moves from Babybear^4 to Goldilocks^2?"
- "What if OpenVM moves from the ethSTARK conjecture to the capacity conjecture?"
- "What if ZisK moves from the ethSTARK conjecture to the provable unique-decoding regime?"

## Results

See the latest results in [`results.md`](results.md).

You can run the calculator by doing `python3 -m soundcalc`

## Supported systems

We currently support the following zkEVMs:
- RISC0
- Miden

We support the following security regimes:
- Unique Decoding Regime (UDR)
- Johnson Bound Regime (JBR)
- Capacity Bound Regime (CBR)
- ethSTARK regime

## Project Layout

- `soundcalc/main.py`: Entry point
- `soundcalc/zkevms/`: One file per supported zkEVM
- `soundcalc/regimes/`: One file per regime (unique decoding, johnson bound, ethSTARK, ...)
- `soundcalc/common/`: Common utilities used by the entire codebase
- `soundcalc/report.py`: Markdown report generator
- `TODO`: A file with TODO tasks!

## Related work

The codebase is heavily based on [RISC0's Python soundness calculator](https://github.com/risc0/risc0/blob/main/risc0/zkp/src/docs/soundness.ipynb).

More inspiration:
- [RISC0 Rust calculator](https://github.com/risc0/risc0/blob/release-2.0/risc0/zkp/src/prove/soundness.rs)
- [`stir-whir-scripts`](https://github.com/WizardOfMenlo/stir-whir-scripts/)
- [Winterfell calculator](https://github.com/facebook/winterfell/blob/main/air/src/proof/security.rs)
- [xkcd](https://xkcd.com/927/)

Based on papers:
- [BCIKS20](https://eprint.iacr.org/2020/654)
- [ethSTARK](https://eprint.iacr.org/2021/582)
- [Ha22](https://eprint.iacr.org/2022/1216)
- [eSTARK](https://eprint.iacr.org/2023/474)
- [RISC0](https://dev.risczero.com/proof-system-in-detail.pdf)

