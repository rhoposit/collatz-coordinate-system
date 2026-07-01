# A Coordinate System for Collatz Dynamics — Code

Code and figure scripts supporting the paper *A Coordinate System for Collatz
Dynamics* (J. Williams). Every result is self-contained. No external data files
or network access are required, since all inputs are generated from the crown
triangle and skeleton formulas in the paper.

## Requirements

Python 3.12.x and the three packages pinned in `requirements.txt`.

```bash
python3 -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

Only `numpy`, `matplotlib`, and `sympy` are used. The verification scripts in
`Section-6.1`, `Section-6.3`, and `Remark-4.6` run on the standard library
alone. `Section-6.4` additionally uses `sympy` for primality of the large
elements.

## Contents

Each script is standalone and run directly, for example
`python3 Section-6.4/verify_primefree_rows.py`. Approximate runtimes are for a
single core and are indicative only.

| Script | Backs in the paper | Runtime |
|---|---|---|
| `Remark-4.6/verify_admissible_counts.py` | Prime-admissible position counts (Remark 4.6, after Cor 4.3) | < 1 s |
| `Section-6.1/crown_asymmetry_analysis.py` | Crown visitation asymmetry, 18.2 per orbit and 93.6 / 6.4 percent split (Observation 6.1) | ~2.5 min |
| `Section-6.2/orbit_27_analysis.py` | Skeleton trajectory of n = 27 and Figure 5 | ~5 s |
| `Section-6.3/chain_length_distribution.py` | Chain count formula and ratio, direct versus formula (Proposition 6.2) | ~1 s |
| `Section-6.4/verify_primefree_rows.py` | Accidentally prime-free rows for k up to 300 (Observation 6.3) | ~5 s |
| `figure1/enumerate_chain_lengths.py` | Chain length distribution data for N = 10^7 (Figure 1) | ~10 s |
| `figure1/plot_chain_lengths_final.py` | Renders Figure 1 | ~10 s |
| `figure3/zero_prime_rows_plot.py` | Renders Figure 3 and prints the prime-count heatmap | ~5 s |
| `figure4/thabit_mersenne_plot.py` | Renders Figure 4 (Mersenne, Thabit, Pierpont, prime density) | ~5 s |

Figure scripts write their PDF and PNG into the same folder. Committed copies of
the figures are included alongside each script.

## Primality testing

`Section-6.4` uses a deterministic Miller-Rabin test with the witness set
`{2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37}` below 2^64 and defers to
`sympy.isprime` above that bound. The figure scripts use `sympy.isprime`
directly, which is deterministic at the sizes involved.

## License

MIT. See `LICENSE`.
