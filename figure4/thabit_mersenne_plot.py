"""
Copyright (c) 2026, Jennifer Williams, University of Southampton
All rights reserved.

This source code is licensed under the MIT License found in the
LICENSE file in the root directory of this source tree.

Contact: Jennifer Williams (j.williams@soton.ac.uk)
"""

from sympy import isprime
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.lines import Line2D

# Colorblind-friendly colors (IBM Design Library)
CB_BLUE = '#648FFF'
CB_PURPLE = '#785EF0'
CB_MAGENTA = '#DC267F'
CB_ORANGE = '#FE6100'
CB_YELLOW = '#FFB000'
CB_GRAY = '#888888'

def edge_B(k, c):
    """Edge B at row k for crown c"""
    return 2**k * (c + 2) - 2

def get_row_elements(k, c):
    """Get all 2k+1 elements in row k of triangle T_c"""
    if k == 0:
        return [c]
    B = edge_B(k, c)
    chain = [B]
    current = B
    for i in range(2*k):
        if current % 2 == 0:
            current = current // 2
        else:
            current = 3 * current + 1
        chain.append(current)
    return chain

# Create figure
fig, axes = plt.subplots(2, 2, figsize=(14, 12))

# Shared x-axis range for row k
max_k = 20
k_ticks = range(0, max_k + 1, 4)

# Get matching y-axis limits for top row
mersenne_max = 2**max_k - 1
thabit_max = 3 * 2**(max_k-1) - 1
y_max = max(mersenne_max, thabit_max) * 1.5
y_min = 0.5

# =============================================================================
# Plot 1 (top left): Mersenne numbers (Position 1) in T_0
# k >= 2 because k=1 gives 2^1-1=1 which is neither prime nor composite
# =============================================================================
ax1 = axes[0, 0]
k_vals_m = list(range(2, max_k + 1))
mersenne_vals = [2**k - 1 for k in k_vals_m]
is_prime_m = [isprime(m) for m in mersenne_vals]

ax1.scatter([k for k, p in zip(k_vals_m, is_prime_m) if not p], 
            [m for m, p in zip(mersenne_vals, is_prime_m) if not p],
            c=CB_GRAY, s=100, label='Composite', alpha=0.5)
ax1.scatter([k for k, p in zip(k_vals_m, is_prime_m) if p], 
            [m for m, p in zip(mersenne_vals, is_prime_m) if p],
            c=CB_BLUE, s=150, label='Prime', marker='*')
ax1.set_yscale('log')
ax1.set_ylim(y_min, y_max)
ax1.set_xlabel('Row $k$', fontsize=12)
ax1.set_ylabel('$2^k - 1$', fontsize=12)
ax1.set_title('Position 1 in $\\mathcal{L}_1$: Mersenne numbers', fontsize=14)
ax1.legend()
ax1.grid(True, alpha=0.3)
ax1.set_xticks(k_ticks)
ax1.set_xlim(0, max_k + 1)

# =============================================================================
# Plot 2 (top right): Thabit numbers (Position 3) in T_0
# =============================================================================
ax2 = axes[0, 1]
# For position 3: k >= 2, and value = 3 * 2^(k-1) - 1
k_vals_t = list(range(2, max_k + 1))
thabit_vals = [3 * 2**(k-1) - 1 for k in k_vals_t]
is_prime_t = [isprime(t) for t in thabit_vals]

ax2.scatter([k for k, p in zip(k_vals_t, is_prime_t) if not p], 
            [t for t, p in zip(thabit_vals, is_prime_t) if not p],
            c=CB_GRAY, s=100, label='Composite', alpha=0.5)
ax2.scatter([k for k, p in zip(k_vals_t, is_prime_t) if p], 
            [t for t, p in zip(thabit_vals, is_prime_t) if p],
            c=CB_ORANGE, s=150, label='Prime', marker='*')
ax2.set_yscale('log')
ax2.set_ylim(y_min, y_max)
ax2.set_xlabel('Row $k$', fontsize=12)
ax2.set_ylabel('$3 \\cdot 2^{k-1} - 1$', fontsize=12)
ax2.set_title('Position 3 in $\\mathcal{L}_1$: Thabit numbers', fontsize=14)
ax2.legend()
ax2.grid(True, alpha=0.3)
ax2.set_xticks(k_ticks)
ax2.set_xlim(0, max_k + 1)

# =============================================================================
# Plot 3 (bottom left): Triangle T_0 showing ALL primes
# x-axis: Row k, y-axis: Position
# =============================================================================
ax3 = axes[1, 0]

max_k_triangle = 20

for k in range(1, max_k_triangle + 1):
    chain = get_row_elements(k, 0)
    for pos in range(1, 2*k, 2):
        val = chain[pos]
        is_p = isprime(val)
        
        if pos == 1:
            # Position 1 (Mersenne: b=0)
            if is_p:
                ax3.scatter(k, pos, c=CB_BLUE, s=200, marker='*', 
                           edgecolors='black', linewidths=0.5)
            else:
                ax3.scatter(k, pos, c=CB_BLUE, s=30, marker='o', alpha=0.3)
        elif pos == 3:
            # Position 3 (Thabit: b=1)
            if is_p:
                ax3.scatter(k, pos, c=CB_ORANGE, s=200, marker='*', 
                           edgecolors='black', linewidths=0.5)
            else:
                ax3.scatter(k, pos, c=CB_ORANGE, s=30, marker='o', alpha=0.3)
        else:
            # Positions 5, 7, 9, ... (b >= 2)
            if is_p:
                ax3.scatter(k, pos, c=CB_GRAY, s=150, marker='*', 
                           edgecolors='black', linewidths=0.5)
            else:
                ax3.scatter(k, pos, c=CB_GRAY, s=20, marker='o', alpha=0.2)

ax3.set_xlabel('Row $k$', fontsize=12)
ax3.set_ylabel('Position', fontsize=12)
ax3.set_title('Pierpont primes (2nd kind) in $\\mathcal{L}_1$: family $2^a \\cdot 3^b - 1$', fontsize=14)

# Legend - upper left
legend_elements = [
    Line2D([0], [0], marker='s', color='w', markerfacecolor=CB_BLUE, 
           markersize=12, label='$b=0$: Mersenne'),
    Line2D([0], [0], marker='s', color='w', markerfacecolor=CB_ORANGE, 
           markersize=12, label='$b=1$: Thabit'),
    Line2D([0], [0], marker='s', color='w', markerfacecolor=CB_GRAY, 
           markersize=12, label='$b \\geq 2$'),
    Line2D([0], [0], marker='*', color='w', markerfacecolor='black', 
           markersize=15, label='Pierpont prime (2nd kind)'),
]
ax3.legend(handles=legend_elements, loc='upper left', fontsize=10)
ax3.grid(True, alpha=0.3)
ax3.set_xticks(k_ticks)
ax3.set_xlim(0, max_k + 1)

ax4 = axes[1, 1]

# Use purple and magenta to distinguish from blue/orange used for Mersenne/Thabit
crowns = [(8, CB_PURPLE, 32.9), (116, CB_MAGENTA, 13.8)]

# Offset positions slightly so they don't overlap
offset = 0.15

for idx, (c, color, density) in enumerate(crowns):
    x_offset = -offset if idx == 0 else offset
    for k in range(1, max_k + 1):
        chain = get_row_elements(k, c)
        for pos in range(1, 2*k, 2):
            val = chain[pos]
            is_p = isprime(val)
            if is_p:
                ax4.scatter(k + x_offset, pos, c=color, s=200, marker='*', 
                          edgecolors='black', linewidths=0.5, zorder=3)
            else:
                ax4.scatter(k + x_offset, pos, c=color, s=30, marker='o', alpha=0.3, zorder=2)

ax4.set_xlabel('Row $k$', fontsize=12)
ax4.set_ylabel('Position', fontsize=12)
ax4.set_title('Prime density: $\\mathcal{L}_5$ (32.9%) vs $\\mathcal{L}_{59}$ (13.8%)', fontsize=14)
ax4.grid(True, alpha=0.3)
ax4.set_xticks(k_ticks)
ax4.set_xlim(0, max_k + 1)
ax4.set_ylim(0, 42)

# Legend - upper left
legend_elements_4 = [
    Line2D([0], [0], marker='s', color='w', markerfacecolor=CB_PURPLE, 
           markersize=12, label='$\\mathcal{L}_5$ (32.9%)'),
    Line2D([0], [0], marker='s', color='w', markerfacecolor=CB_MAGENTA, 
           markersize=12, label='$\\mathcal{L}_{59}$ (13.8%)'),
    Line2D([0], [0], marker='*', color='w', markerfacecolor='black', 
           markersize=15, label='Prime'),
]
ax4.legend(handles=legend_elements_4, loc='upper left', fontsize=10)

plt.tight_layout()
plt.savefig('thabit_mersenne_figure.pdf', bbox_inches='tight')
plt.savefig('thabit_mersenne_figure.png', dpi=150, bbox_inches='tight')
print("Saved thabit_mersenne_figure.pdf and .png")
