#!/usr/bin/env python3
"""
Copyright (c) 2026, Jennifer Williams, University of Southampton
All rights reserved.

This source code is licensed under the MIT License found in the
LICENSE file in the root directory of this source tree.

Contact: Jennifer Williams (j.williams@soton.ac.uk)
"""

def is_dos_obstructed(a, b):
    """Difference of squares: both a and b even"""
    return (a % 2 == 0) and (b % 2 == 0)

def is_div5_obstructed(a, b):
    """Divisibility by 5: both odd and a ≡ b (mod 4)"""
    if (a % 2 == 1) and (b % 2 == 1):
        return (a % 4) == (b % 4)
    return False

def is_prime_admissible(a, b):
    """Position is prime-admissible if it escapes both obstructions"""
    return not is_dos_obstructed(a, b) and not is_div5_obstructed(a, b)

def count_admissible_in_row(k):
    """
    Row k has positions (a, b) with a + b = k, a >= 1, b >= 0.
    So b = 0, 1, ..., k-1 and a = k, k-1, ..., 1.
    Total: k positions.
    """
    admissible = []
    obstructed_dos = []
    obstructed_div5 = []
    
    for b in range(k):  # b = 0, 1, ..., k-1
        a = k - b       # a = k, k-1, ..., 1
        
        dos = is_dos_obstructed(a, b)
        div5 = is_div5_obstructed(a, b)
        
        if dos:
            obstructed_dos.append((a, b))
        if div5:
            obstructed_div5.append((a, b))
        if not dos and not div5:
            admissible.append((a, b))
    
    return admissible, obstructed_dos, obstructed_div5

def main():
    print("Verifying prime-admissible position counts (Remark 4.6)")
    print("=" * 70)
    
    # Test specific examples for each class
    test_cases = {
        "k odd": list(range(1, 43, 2)),            # 1, 3, 5, ..., 41
        "k ≡ 0 (mod 4)": list(range(4, 43, 4)),    # 4, 8, 12, ..., 40
        "k ≡ 2 (mod 4)": list(range(2, 43, 4)),    # 2, 6, 10, ..., 42
    }    
    
    all_pass = True
    
    for class_name, k_values in test_cases.items():
        print(f"\n{class_name}:")
        print("-" * 70)
        
        for k in k_values:
            admissible, dos, div5 = count_admissible_in_row(k)
            n_admissible = len(admissible)
            n_total = k
            
            # Determine expected count
            if k % 2 == 1:
                expected = k
                expected_str = f"k = {k}"
            elif k % 4 == 0:
                expected = k // 2
                expected_str = f"k/2 = {k//2}"
            elif k % 4 == 2 and k >= 6:
                expected = 0
                expected_str = "0"
            else:
                expected = None
                expected_str = "N/A"
            
            match = (n_admissible == expected) if expected is not None else True
            status = "✓" if match else "✗"
            
            if not match:
                all_pass = False
            
            print(f"  k={k:3d}: {n_admissible:3d} admissible / {n_total:3d} total "
                  f"(expected {expected_str}) {status}")
            
            # Show details for small k or failures
            if k <= 8 or not match:
                print(f"         DoS obstructed: {dos}")
                print(f"         Div5 obstructed: {div5}")
                print(f"         Admissible: {admissible}")
    
    # Summary
    print("\n" + "=" * 70)
    print("VERIFICATION SUMMARY")
    print("=" * 70)
    
    if all_pass:
        print("\n✓ All claims in Remark 4.6 verified correctly!")
    else:
        print("\n✗ Some claims failed verification - check above for details")
    
    # Show the pattern explicitly
    print("\n" + "=" * 70)
    print("DETAILED BREAKDOWN FOR k = 1 to 20")
    print("=" * 70)
    print(f"{'k':>3} {'class':>12} {'total':>6} {'admit':>6} {'DoS':>6} {'div5':>6} {'expected':>10}")
    print("-" * 70)
    
    for k in range(1, 21):
        admissible, dos, div5 = count_admissible_in_row(k)
        
        if k % 2 == 1:
            cls = "odd"
            exp = f"k={k}"
        elif k % 4 == 0:
            cls = "≡0 (mod 4)"
            exp = f"k/2={k//2}"
        else:
            cls = "≡2 (mod 4)"
            exp = "0" if k >= 6 else "special"
        
        print(f"{k:3d} {cls:>12} {k:>6} {len(admissible):>6} {len(dos):>6} {len(div5):>6} {exp:>10}")

if __name__ == "__main__":
    main()
