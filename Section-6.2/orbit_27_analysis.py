#!/usr/bin/env python3
"""
Copyright (c) 2026, Jennifer Williams, University of Southampton
All rights reserved.

This source code is licensed under the MIT License found in the
LICENSE file in the root directory of this source tree.

Contact: Jennifer Williams (j.williams@soton.ac.uk)
"""

import matplotlib.pyplot as plt
import numpy as np

def get_crown(n):
    """Find which crown n belongs to."""
    if n == 0:
        return 0
    if n in (1, 2, 4):
        return 0
    current = n
    for _ in range(10000):
        if current % 12 == 0 or current % 12 == 8:
            return current
        if current % 2 == 0:
            current = current // 2
        else:
            current = 3 * current + 1
        if current in (1, 2, 4):
            return 0
    raise ValueError(f"Max steps exceeded from {n}")

def collatz_step(n):
    if n % 2 == 0:
        return n // 2
    else:
        return 3 * n + 1

def get_lambda_trajectory(n):
    """
    Get the lambda value at each step of the Collatz orbit.
    Returns list of (step, lambda_value) pairs.
    """
    trajectory = []
    current = n
    step = 0
    
    while current != 1:
        crown = get_crown(current)
        lam = (crown + 2) // 2
        trajectory.append((step, lam, current))
        current = collatz_step(current)
        step += 1
    
    # Terminal
    trajectory.append((step, 1, current))
    return trajectory

def plot_orbit_comparison(save_path='orbit_27_figure.pdf'):
    """
    Create figure comparing orbit of 27 to typical orbits.
    """
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5))
    
    # Left panel: Lambda trajectory over Collatz steps
    trajectories = {
        7: '#3498db',      # blue
        15: '#2ecc71',     # green  
        27: '#e74c3c',     # red (highlighted)
        127: '#9b59b6',    # purple
    }
    
    for n, color in trajectories.items():
        traj = get_lambda_trajectory(n)
        steps = [t[0] for t in traj]
        lambdas = [t[1] for t in traj]
        
        linewidth = 3 if n == 27 else 1.5
        alpha = 1.0 if n == 27 else 0.7
        ax1.plot(steps, lambdas, color=color, linewidth=linewidth, 
                 alpha=alpha, label=f'n = {n}')
        ax1.scatter(steps, lambdas, color=color, s=20 if n == 27 else 10, 
                    alpha=alpha, zorder=5)
    
    ax1.set_yscale('log')
    ax1.set_xlabel('Collatz step', fontsize=12)
    ax1.set_ylabel(r'Skeleton $\lambda$', fontsize=12)
    ax1.set_title(r'Skeleton trajectory: $\lambda$ value at each Collatz step', fontsize=12)
    ax1.legend(loc='upper right')
    ax1.grid(True, alpha=0.3)
    
    # Right panel: Distribution of max lambda for small n
    max_lambdas = []
    n_values = list(range(3, 201))
    
    for n in n_values:
        traj = get_lambda_trajectory(n)
        max_lam = max(t[1] for t in traj)
        max_lambdas.append(max_lam)
    
    # Color bars: highlight 27
    colors = ['#e74c3c' if n == 27 else '#3498db' for n in n_values]
    
    ax2.bar(n_values, max_lambdas, color=colors, edgecolor='none', alpha=0.7)
    ax2.axhline(y=max_lambdas[n_values.index(27)], color='#e74c3c', 
                linestyle='--', linewidth=2, label=f'n = 27 (max λ = {max_lambdas[n_values.index(27)]})')
    
    ax2.set_yscale('log')
    ax2.set_xlabel('Starting value $n$', fontsize=12)
    ax2.set_ylabel(r'Maximum $\lambda$ visited', fontsize=12)
    ax2.set_title(r'Maximum skeleton $\lambda$ reached by each orbit', fontsize=12)
    ax2.legend(loc='upper right')
    ax2.grid(True, alpha=0.3, axis='y')
    
    plt.tight_layout()
    plt.savefig(save_path, dpi=150, bbox_inches='tight')
    plt.savefig(save_path.replace('.pdf', '.png'), dpi=150, bbox_inches='tight')
    plt.close()
    print(f"Saved: {save_path}")

def print_analysis():
    """Print analysis for the paper text."""
    print("=" * 70)
    print("ANALYSIS OF 27's ORBIT")
    print("=" * 70)
    
    # Basic facts
    traj_27 = get_lambda_trajectory(27)
    max_val = max(t[2] for t in traj_27)
    max_lam = max(t[1] for t in traj_27)
    num_steps = len(traj_27)-1
    
    print(f"\nOrbit of 27:")
    print(f"  Number of steps: {num_steps}")
    print(f"  Maximum value reached: {max_val}")
    print(f"  Maximum lambda visited: {max_lam}")
    
    # Crown 27 belongs to
    crown_27 = get_crown(27)
    lambda_27 = (crown_27 + 2) // 2
    print(f"\n27 next crown reached (extended λ assignment):")
    print(f"  Crown: {crown_27}")
    print(f"  Lambda: {lambda_27}")
    
    # Distinct skeletons visited (globally unique, in order of first appearance)
    seen = set()
    distinct_lambdas = []
    for step, lam, val in traj_27:
        if lam not in seen:
            seen.add(lam)
            distinct_lambdas.append(lam)

    print(f"\nDistinct skeletons visited (in order of first appearance):")
    print(f"  λ values: {distinct_lambdas}")
    print(f"  Number of distinct skeletons: {len(distinct_lambdas)}")
    
    # Compare to typical
    print(f"\nComparison with nearby starting values:")
    for n in [7, 15, 26, 27, 28, 31, 63]:
        traj = get_lambda_trajectory(n)
        max_l = max(t[1] for t in traj)
        crown = get_crown(n)
        start_lam = (crown + 2) // 2
        print(f"  n = {n:>3}: starts in λ = {start_lam:>4}, max λ = {max_l:>4}")


if __name__ == "__main__":
    print_analysis()
    print()
    print("Generating figure...")
    plot_orbit_comparison('orbit_27_figure.pdf')
