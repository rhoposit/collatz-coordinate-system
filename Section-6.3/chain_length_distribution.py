#!/usr/bin/env python3
"""
Copyright (c) 2026, Jennifer Williams, University of Southampton
All rights reserved.

This source code is licensed under the MIT License found in the
LICENSE file in the root directory of this source tree.

Contact: Jennifer Williams (j.williams@soton.ac.uk)
"""

import math


def get_row_elements(c, k):
    """
    Get all elements in row k of triangle T_c via Collatz iteration.
    Row k has 2k+1 elements (a chain of length 2k+1).
    """
    if k == 0:
        return [c]
    B_k = (2 ** k) * (c + 2) - 2
    chain = [B_k]
    current = B_k
    for _ in range(2 * k):
        if current % 2 == 0:
            current = current // 2
        else:
            current = 3 * current + 1
        chain.append(current)
    return chain


def count_valid_lambdas(max_lambda):
    """
    Count integers up to max_lambda that are coprime to 6.
    These are the valid λ values (λ ≡ 1 or 5 mod 6).
    """
    count = 0
    for lam in range(1, int(max_lambda) + 1):
        if math.gcd(lam, 6) == 1:
            count += 1
    return count


def R_k_direct(N, k, max_crowns=100000):
    """
    Directly count R_k(N): number of row-k chains that intersect [0, N].
    """
    count = 0
    for c in range(0, max_crowns, 12):  # c ≡ 0 (mod 12)
        row = get_row_elements(c, k)
        if min(row) <= N:
            count += 1
    for c in range(8, max_crowns, 12):  # c ≡ 8 (mod 12)
        row = get_row_elements(c, k)
        if min(row) <= N:
            count += 1
    return count


def R_k_formula(N, k):
    """
    Compute R_k(N) via the formula.
    
    Row k intersects [0, N] when min(row k) = 2^k · λ - 1 ≤ N,
    giving λ ≤ (N+1) / 2^k.
    """
    max_lambda = (N + 1) / (2**k)
    return count_valid_lambdas(max_lambda)


def theoretical_R_k(N, k):
    """
    Theoretical asymptotic value: R_k(N) = N / (6 · 2^(k-1)).
    """
    return N / (6 * 2**(k-1))


def verify_proposition(N_values=None, k_values=None):
    """
    Verify the proposition for various N and k values.
    """
    if N_values is None:
        N_values = [1000, 10000, 100000, 1000000]
    if k_values is None:
        k_values = [2, 3, 4, 5, 6]
    
    print("=" * 80)
    print("VERIFICATION: R_k(N) = N / (6 · 2^(k-1)) + O(1)")
    print("=" * 80)
    
    for N in N_values:
        print(f"\nN = {N:,}")
        print("-" * 70)
        print(f"{'k':<5} {'Direct':<12} {'Formula':<12} {'Theoretical':<15} {'Ratio':<10}")
        
        results = {}
        for k in k_values:
            # Direct computation (only for smaller N)
            if N <= 10000:
                direct = R_k_direct(N, k, max_crowns=N * 10)
            else:
                direct = "—"
            
            formula = R_k_formula(N, k)
            theoretical = theoretical_R_k(N, k)
            results[k] = formula
            
            # Ratio to next k
            ratio_str = ""
            if k > min(k_values) and results.get(k-1, 0) > 0 and formula > 0:
                ratio = results[k-1] / formula
                ratio_str = f"{ratio:.4f}"
            
            print(f"{k:<5} {str(direct):<12} {formula:<12} {theoretical:<15.2f} {ratio_str:<10}")
    
    # Verify ratio convergence
    print("\n" + "=" * 80)
    print("RATIO VERIFICATION: R_k(N) / R_{k+1}(N) → 2 as N → ∞")
    print("=" * 80)
    print(f"\n{'N':<15} {'R_2/R_3':<12} {'R_3/R_4':<12} {'R_4/R_5':<12}")
    print("-" * 55)
    
    for N in [1000, 10000, 100000, 1000000, 10000000]:
        ratios = []
        for k in [2, 3, 4]:
            r_k = R_k_formula(N, k)
            r_k1 = R_k_formula(N, k + 1)
            ratio = r_k / r_k1 if r_k1 > 0 else float('inf')
            ratios.append(f"{ratio:.4f}")
        print(f"{N:<15} {ratios[0]:<12} {ratios[1]:<12} {ratios[2]:<12}")


def verify_row_structure():
    """
    Verify the structure of rows and edge formulas.
    """
    print("\n" + "=" * 80)
    print("ROW STRUCTURE VERIFICATION")
    print("=" * 80)
    
    print("\nRow elements for selected crowns and k values:")
    print("-" * 70)
    
    for c in [0, 8, 12, 20]:
        lam = (c + 2) // 2
        print(f"\nCrown c = {c}, λ = {lam}:")
        for k in [1, 2, 3]:
            row = get_row_elements(c, k)
            print(f"  k = {k}: {row}")
            print(f"         min = {min(row)} at position {row.index(min(row))}")
            print(f"         position 0 = {row[0]} = 2(2^{k}·{lam} - 1) = {2*(2**k * lam - 1)}")


if __name__ == "__main__":
    verify_row_structure()
    print()
    verify_proposition()
