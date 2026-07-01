#!/usr/bin/env python3
"""
Copyright (c) 2026, Jennifer Williams, University of Southampton
All rights reserved.

This source code is licensed under the MIT License found in the
LICENSE file in the root directory of this source tree.

Contact: Jennifer Williams (j.williams@soton.ac.uk)
"""

def get_distinct_crowns(n):
    """
    Get sets of distinct crowns visited by Collatz orbit from n.
    Returns (set of 0mod12 crowns, set of 8mod12 crowns).
    """
    crowns_0mod12 = set()
    crowns_8mod12 = set()
    current = n
    
    while current != 1:
        mod = current % 12
        if mod == 0:
            crowns_0mod12.add(current)
        elif mod == 8:
            crowns_8mod12.add(current)
        
        if current % 2 == 0:
            current = current // 2
        else:
            current = 3 * current + 1
    
    crowns_0mod12.add(0)  # Terminal: 1, 2, 4 belong to crown 0
    return crowns_0mod12, crowns_8mod12


def analyze_crown_asymmetry(max_n=10_000_000, report_interval=1_000_000):
    """
    Analyze crown visitation asymmetry for orbits starting from n = 1 to max_n.
    """
    print(f"Analyzing crown visitation for n = 1 to {max_n:,}")
    print("=" * 70)
    
    total_distinct_0mod12 = 0
    total_distinct_8mod12 = 0
    
    for n in range(1, max_n + 1):
        c0, c8 = get_distinct_crowns(n)
        total_distinct_0mod12 += len(c0)
        total_distinct_8mod12 += len(c8)
        
        if n % report_interval == 0:
            total = total_distinct_0mod12 + total_distinct_8mod12
            pct_8 = 100 * total_distinct_8mod12 / total
            print(f"  n = {n:>10,}: 8mod12 = {pct_8:.1f}%")
    
    # Final results
    total_crowns = total_distinct_0mod12 + total_distinct_8mod12
    avg_per_orbit = total_crowns / max_n
    pct_0mod12 = 100 * total_distinct_0mod12 / total_crowns
    pct_8mod12 = 100 * total_distinct_8mod12 / total_crowns
    
    print()
    print("=" * 70)
    print("RESULTS")
    print("=" * 70)
    print(f"Total distinct crown visits: {total_crowns:,}")
    print(f"  - 0mod12: {total_distinct_0mod12:,} ({pct_0mod12:.1f}%)")
    print(f"  - 8mod12: {total_distinct_8mod12:,} ({pct_8mod12:.1f}%)")
    print(f"Average distinct crowns per orbit: {avg_per_orbit:.1f}")
    print(f"Sum of percentages: {pct_0mod12 + pct_8mod12:.1f}%")
    
    # Count crown density in the range
    num_crowns_0mod12 = len([c for c in range(0, max_n + 1) if c % 12 == 0])
    num_crowns_8mod12 = len([c for c in range(0, max_n + 1) if c % 12 == 8])
    
    print()
    print(f"CROWN DENSITY (integers from 0 to {max_n:,}):")
    print(f"  Crowns with c ≡ 0 (mod 12): {num_crowns_0mod12:,}")
    print(f"  Crowns with c ≡ 8 (mod 12): {num_crowns_8mod12:,}")
    print(f"  Ratio: {num_crowns_8mod12 / num_crowns_0mod12:.4f} (equal density)")
    
    return {
        'max_n': max_n,
        'total_0mod12': total_distinct_0mod12,
        'total_8mod12': total_distinct_8mod12,
        'avg_per_orbit': avg_per_orbit,
        'pct_0mod12': pct_0mod12,
        'pct_8mod12': pct_8mod12,
    }


if __name__ == "__main__":
    results = analyze_crown_asymmetry(max_n=10_000_000)
