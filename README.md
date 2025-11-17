![](assets/logo.png)
# soundcalc

🚧 **WIP right now. Please give us some time.** 🚧

A universal soundness calculator across FRI-based zkEVM proof systems and security regimes.

It aims to answer questions like:
- "What if RISC0 moves from Babybear⁴ to Goldilocks³?"
- "What if OpenVM moves from the Toy Problem heuristic to the provable Johnson Bound Regime?"
- "What if ZisK moves from the Toy Problem heuristic to the provable Unique Decoding Regime?"

## Results

See the latest results in [`results.md`](results.md).

You can run the calculator by doing `python3 -m soundcalc`.
As a result, the calculator generates / updates [`results.md`](results.md).

## Supported systems

We currently support the following zkEVMs:
- RISC0
- Miden
- ZisK

We support the following security regimes (see below for explanation of regimes):
- Unique Decoding Regime (UDR)
- Johnson Bound Regime (JBR)

In addition, we give a number based on the ethstark toy problem conjecture for reference.

## Background on Security Regimes

Consider a fixed set of parameters describing the prover and verifier of a FRI-based zkEVM.
To evaluate the *concrete soundness level* of such a system, we introduce a parameter `θ` in the range `(0, 1)`.

The soundness level is then determined as a function of `θ` and the zkEVM parameters (e.g., field size, code rate).
Depending on the value of `θ`, the analysis falls into different regimes:

- **UDR (Unique Decoding Regime):** $\theta  \leq  (1 - \rho)/2$, where $\rho$ is the code rate.
- **JBR (Johnson Bound Regime):** $(1 - \rho)/2 < \theta < 1 - \sqrt{\rho}$.

Crucially, `θ` is not an input to the prover or verifier code—it is only used in the *soundness analysis*.
All three regimes therefore apply to the *same zkEVM instance* without any change.

We also output the security level estimated by considering the currently best known attack.
Here, we currently follow the **Toy Problem Regime (TPR) / ethSTARK conjecture**.

## Incorporation of recent work

A flurry of new results on proximity gaps were published in November 2025 (see [Nico's summary](https://blog.zksecurity.xyz/posts/proximity-conjecture/)).

In soundcalc we have incorporated:
- The [improved JBR security bounds](https://github.com/asn-d6/soundcalc/commit/0f91fba90661af1a7c9fa6114e6eb41e79d18ebf) of [BGHKS25](https://eprint.iacr.org/2025/2055.pdf)
- The [removal of the CBR regime](https://github.com/asn-d6/soundcalc/commit/ffaeb81dbb450b7c905c90338af8304c2bbfeb60), following the results of [DG25](https://eprint.iacr.org/2025/2010.pdf) and [CS25](https://eprint.iacr.org/2025/2046.pdf)

## Project Layout

- `soundcalc/main.py`: Entry point
- `soundcalc/zkevms/`: One file per supported zkEVM
- `soundcalc/regimes/`: One file per regime (unique decoding, johnson bound, ...)
- `soundcalc/common/`: Common utilities used by the entire codebase
- `soundcalc/report.py`: Markdown report generator

## Related work

The codebase is heavily based on [RISC0's Python soundness calculator](https://github.com/risc0/risc0/blob/main/risc0/zkp/src/docs/soundness.ipynb).

More inspiration:
- [RISC0 Rust calculator](https://github.com/risc0/risc0/blob/release-2.0/risc0/zkp/src/prove/soundness.rs)
- [`stir-whir-scripts`](https://github.com/WizardOfMenlo/stir-whir-scripts/)
- [Winterfell calculator](https://github.com/facebook/winterfell/blob/main/air/src/proof/security.rs)
- [xkcd](https://xkcd.com/927/)

Based on papers (links point to specific versions where possible):
- [BCIKS20](https://eprint.iacr.org/archive/2020/654/20210703:203025)
- [ethSTARK](https://eprint.iacr.org/archive/2021/582/20250608:155119)
- [Ha22](https://eprint.iacr.org/archive/2022/1216/20241217:162441)
- [eSTARK](https://eprint.iacr.org/archive/2023/474/20230331:165019)
- [RISC0](https://dev.risczero.com/proof-system-in-detail.pdf)
