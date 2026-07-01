#!/usr/bin/env python3
"""
Copyright (c) 2026, Jennifer Williams, University of Southampton
All rights reserved.

This source code is licensed under the MIT License found in the
LICENSE file in the root directory of this source tree.

Contact: Jennifer Williams (j.williams@soton.ac.uk)
"""

import numpy as np
import matplotlib.pyplot as plt
import sympy
from matplotlib.colors import LinearSegmentedColormap

#==============================================================================
# Core Functions
#==============================================================================

def crown_to_lambda(c):
    """Convert crown c to λ-parameter: λ = (c + 2) / 2"""
    return (c + 2) // 2

def lambda_to_crown(lam):
    """Convert λ-parameter to crown c: c = 2λ - 2"""
    return 2 * lam - 2

def is_crown(n):
    """Check if n is a crown (n ≡ 0 or 8 mod 12)."""
    return n % 12 == 0 or n % 12 == 8

def get_row_elements(c, k):
    """
    Get all elements in row k of triangle with crown c.
    Row k has 2k+1 elements (for k >= 1) forming a Collatz chain.
    The base element is B_k = 2^k * (c + 2) - 2.
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

def count_primes_in_row(c, k):
    """Count primes in row k of triangle with crown c."""
    elements = get_row_elements(c, k)
    odd_elements = [e for e in elements if e % 2 == 1]
    return sum(1 for e in odd_elements if sympy.isprime(e))

#==============================================================================
# Plotting
#==============================================================================

def plot_zero_prime_rows(save_path='zero_prime_rows.pdf'):
    """
    Create 2-panel figure showing zero-prime row phenomenon.
    
    Left panel: Bar chart of prime counts per row in skeleton λ=1
    Right panel: Heatmap of prime counts in rows k ≡ 2 (mod 4) across skeletons
    """
    
    # Parameters matching the original figure
    max_row_left = 35      # rows 0 to 35 for left panel
    max_row_right = 38     # k values up to 38 for right panel
    
    # λ values to test (first 11 skeletons)
    lambda_values = [1, 5, 7, 11, 13, 17, 19, 23, 25, 29, 31]
    
    # Rows k ≡ 2 (mod 4) for right panel
    k_values_mod2 = [k for k in range(2, max_row_right + 1, 4)]  # 2, 6, 10, 14, ...
    
    #==========================================================================
    # Left Panel Data: Prime counts per row in λ=1 skeleton
    # Show all rows to display the full pattern
    #==========================================================================
    c_lambda1 = lambda_to_crown(1)  # c = 0
    
    row_indices = list(range(0, max_row_left + 1))
    prime_counts_left = []
    is_k_mod2_of_4 = []
    
    for k in row_indices:
        count = count_primes_in_row(c_lambda1, k)
        prime_counts_left.append(count)
        is_k_mod2_of_4.append(k % 4 == 2)
    
    #==========================================================================
    # Right Panel Data: Heatmap across skeletons
    #==========================================================================
    heatmap_data = []
    
    for lam in lambda_values:
        c = lambda_to_crown(lam)
        row_data = []
        for k in k_values_mod2:
            count = count_primes_in_row(c, k)
            row_data.append(count)
        heatmap_data.append(row_data)
    
    heatmap_array = np.array(heatmap_data)
    
    #==========================================================================
    # Create Figure
    #==========================================================================
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5))
    
    #--- Left Panel: Bar chart ---
    # Orange for k ≡ 2 (mod 4), blue for other rows
    colors_left = ['#e67e22' if mod2 else '#3498db' for mod2 in is_k_mod2_of_4]
    
    bars = ax1.bar(row_indices, prime_counts_left, color=colors_left, edgecolor='black', linewidth=0.5)
    
    # Add "0" labels on the zero-prime bars for k ≡ 2 (mod 4), k >= 6
    for k, count in zip(row_indices, prime_counts_left):
        if k >= 6 and k % 4 == 2 and count == 0:
            ax1.text(k, 0.1, '0', ha='center', va='bottom', fontsize=9, color='#e67e22', fontweight='bold')
    
    # Set x-axis range and ticks to match right panel
    ax1.set_xlim(-1, 39)
    ax1.set_xticks(k_values_mod2)  # 2, 6, 10, 14, ..., 38
    
    ax1.set_xlabel(r'Row $k$', fontsize=12)
    ax1.set_ylabel('Number of primes in row', fontsize=12)
    ax1.set_title(r'Prime counts per row in $\mathcal{L}_1$' + '\n' + r'(Orange: $k \equiv 2$ (mod 4), all zero for $k \geq 6$)', fontsize=11)
    ax1.legend([plt.Rectangle((0,0),1,1, color='#e67e22'), 
                plt.Rectangle((0,0),1,1, color='#3498db')],
               [r'$k \equiv 2$ (mod 4)', 'Other rows'], loc='upper left')
    
    #--- Right Panel: Heatmap ---
    cmap = plt.cm.YlOrRd
    
    im = ax2.imshow(heatmap_array, aspect='auto', cmap=cmap, vmin=0)
    
    # Add a green line under λ=1 row to highlight it
    ax2.axhline(y=0.5, color='green', linewidth=3)
    
    # Set tick labels
    ax2.set_xticks(range(len(k_values_mod2)))
    ax2.set_xticklabels(k_values_mod2)
    ax2.set_yticks(range(len(lambda_values)))
    ax2.set_yticklabels(lambda_values)
    
    ax2.set_xlabel(r'Row $k$ ($k \equiv 2$ mod 4)', fontsize=12)
    ax2.set_ylabel(r'$\mathcal{L}_\lambda$', fontsize=12)
    ax2.set_title(r'Prime counts in rows $k \equiv 2$ (mod 4): $\mathcal{L}_1$ is uniquely zero', fontsize=11)
    
    # Add text annotations in cells
    for i in range(len(lambda_values)):
        for j in range(len(k_values_mod2)):
            val = heatmap_array[i, j]
            # Choose text color based on background
            text_color = 'white' if val > 4 else 'black'
            ax2.text(j, i, str(int(val)), ha='center', va='center', 
                     fontsize=9, color=text_color, fontweight='bold')
    
    # Colorbar
    cbar = plt.colorbar(im, ax=ax2, shrink=0.8)
    cbar.set_label('Prime count', fontsize=11)
    
    plt.tight_layout()
    plt.savefig(save_path, dpi=150, bbox_inches='tight')
    plt.close()
    print(f"Saved: {save_path}")
    
    return heatmap_array, lambda_values, k_values_mod2

#==============================================================================
# Main
#==============================================================================

if __name__ == "__main__":
    print("Generating zero-prime rows figure with corrected notation...")
    heatmap, lambdas, ks = plot_zero_prime_rows('zero_prime_rows.pdf')
    
    # Print summary
    print("\nHeatmap summary:")
    print(f"  Skeletons (λ values): {lambdas}")
    print(f"  Rows tested: {ks}")
    print(f"  λ=1 row (should be all zeros for k>=6): {list(heatmap[0])}")
    print(f"  Total (skeleton, row) pairs tested: {len(lambdas) * len(ks)}")
    
    print("\nDone.")
