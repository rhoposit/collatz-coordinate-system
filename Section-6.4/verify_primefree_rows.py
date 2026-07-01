#!/usr/bin/env python3
"""
Copyright (c) 2026, Jennifer Williams, University of Southampton
All rights reserved.

This source code is licensed under the MIT License found in the
LICENSE file in the root directory of this source tree.

Contact: Jennifer Williams (j.williams@soton.ac.uk)
"""
import sympy

def miller_rabin(n, witnesses=None):
    """Miller-Rabin primality test"""
    if n < 2:
        return False
    if n == 2 or n == 3:
        return True
    if n % 2 == 0:
        return False
    
    # Write n-1 as 2^r * d
    r, d = 0, n - 1
    while d % 2 == 0:
        r += 1
        d //= 2
    
    # Witnesses sufficient for n < 3,317,044,064,679,887,385,961,981
    if witnesses is None:
        witnesses = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37]
    
    for a in witnesses:
        if a >= n:
            continue
        x = pow(a, d, n)
        if x == 1 or x == n - 1:
            continue
        for _ in range(r - 1):
            x = pow(x, 2, n)
            if x == n - 1:
                break
        else:
            return False
    return True

# Deterministic Miller-Rabin: the witness set {2,...,37} (first 12 primes)
# is a certified test for all n < 2^64 (Sorenson & Webster 2017; OEIS A014233).
MR_DETERMINISTIC_BOUND = 2**64

def is_prime(n):
    # Below the bound, the 12-witness Miller-Rabin is a deterministic proof.
    # Above it, that witness set is no longer certified, so defer to
    # sympy.isprime (BPSW: strong Fermat base 2 + strong Lucas), which has
    # no known counterexamples.
    if n < MR_DETERMINISTIC_BOUND:
        return miller_rabin(n)
    return sympy.isprime(n)

def row_elements(k):
    """Return all elements in row k of L_1: {2^a * 3^b - 1 : a+b=k, a>=1}"""
    elements = []
    for b in range(k):  # b = 0, 1, ..., k-1
        a = k - b       # a = k, k-1, ..., 1
        n = (2**a) * (3**b) - 1
        elements.append((a, b, n))
    return elements

def count_primes_in_row(k):
    """Count primes in row k of L_1"""
    primes = []
    for a, b, n in row_elements(k):
        if is_prime(n):
            primes.append((a, b, n))
    return primes

def main():
    max_k = 300
    
    # Track prime-free rows by residue class
    accidentally_primefree_mod0 = []  # k ≡ 0 (mod 4)
    accidentally_primefree_odd = []    # k odd
    algebraically_primefree = []       # k ≡ 2 (mod 4), k >= 6
    
    print("Scanning rows k = 1 to", max_k)
    print("=" * 60)
    
    for k in range(1, max_k + 1):
        primes = count_primes_in_row(k)
        num_primes = len(primes)
        
        if k % 4 == 2:
            # Algebraically prime-free (should have 0 primes for k >= 6)
            if k >= 6:
                algebraically_primefree.append(k)
                if num_primes > 0:
                    print(f"WARNING: k={k} (algebraic) has {num_primes} primes: {primes}")
        else:
            # Could be accidentally prime-free
            if num_primes == 0:
                if k % 2 == 1 and k >= 3:
                    accidentally_primefree_odd.append(k)
                elif k % 4 == 0:
                    accidentally_primefree_mod0.append(k)
    
    print("\n" + "=" * 60)
    print("RESULTS")
    print("=" * 60)
    
    # Algebraically prime-free verification
    print(f"\nAlgebraically prime-free rows (k ≡ 2 mod 4, k >= 6):")
    print(f"  Count: {len(algebraically_primefree)} rows")
    
    # Accidentally prime-free: k ≡ 0 (mod 4)
    total_mod0 = len([k for k in range(4, max_k + 1, 4)])
    print(f"\nAccidentally prime-free rows (k ≡ 0 mod 4):")
    print(f"  Rows: {accidentally_primefree_mod0}")
    print(f"  Count: {len(accidentally_primefree_mod0)} out of {total_mod0}")
    print(f"  Percentage: {100*len(accidentally_primefree_mod0)/total_mod0:.1f}%")
    
    # Accidentally prime-free: k odd
    total_odd = len([k for k in range(3, max_k + 1, 2)])
    print(f"\nAccidentally prime-free rows (k odd):")
    print(f"  Rows: {accidentally_primefree_odd}")
    print(f"  Count: {len(accidentally_primefree_odd)} out of {total_odd}")
    print(f"  Percentage: {100*len(accidentally_primefree_odd)/total_odd:.1f}%")
    
    # Comparison with claimed values
    print("\n" + "=" * 60)
    print("COMPARISON WITH PAPER CLAIMS")
    print("=" * 60)
    claimed_mod0 = [84, 100, 116, 156, 176, 184, 188, 200, 252, 284, 300]
    claimed_odd = [149, 165, 261]
    
    print(f"\nk ≡ 0 (mod 4):")
    print(f"  Claimed: {claimed_mod0}")
    print(f"  Found:   {accidentally_primefree_mod0}")
    print(f"  Match:   {claimed_mod0 == accidentally_primefree_mod0}")
    
    print(f"\nk odd:")
    print(f"  Claimed: {claimed_odd}")
    print(f"  Found:   {accidentally_primefree_odd}")
    print(f"  Match:   {claimed_odd == accidentally_primefree_odd}")

if __name__ == "__main__":
    main()
