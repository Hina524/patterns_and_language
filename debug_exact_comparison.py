#!/usr/bin/env python3
from pattern_finder import PatternFinder

# Create a pattern finder instance
finder = PatternFinder(level=3)

# Test sequences from our failed tests
test7_seq1 = [('Running', 'VP'), ('quickly', 'ADVP'), ('exhausted', 'VP'), ('him', 'NP'), ('completely', 'ADVP')]
test7_seq2 = [('Swimming', 'NP'), ('slowly', 'ADVP'), ('relaxed', 'VP'), ('her', 'NP'), ('totally', 'ADVP')]

test8_seq1 = [('She', 'NP'), ('seems', 'VP'), ('very', 'ADJP'), ('happy', 'ADJP'), ('today', 'O')]
test8_seq2 = [('He', 'NP'), ('looks', 'VP'), ('quite', 'ADJP'), ('tired', 'ADJP'), ('now', 'ADVP')]

# Let's trace through what find_common_patterns is actually doing
print("="*60)
print("Understanding the pattern matching logic")
print("="*60)

# The algorithm compares tuples - let's see what it's comparing
print("\nTest 7 - Checking for exact tuple matches:")
print(f"Seq1: {test7_seq1}")
print(f"Seq2: {test7_seq2}")

# Check all possible patterns from seq1
for length in range(len(test7_seq1), 0, -1):
    for start in range(len(test7_seq1) - length + 1):
        pattern = tuple(test7_seq1[start:start + length])
        
        # Check if this exact pattern exists in seq2
        found = False
        for i in range(len(test7_seq2) - length + 1):
            if tuple(test7_seq2[i:i + length]) == pattern:
                found = True
                formatted = finder.format_pattern(pattern)
                print(f"\nFOUND MATCH: '{formatted}'")
                print(f"  Pattern: {pattern}")
                print(f"  Found at position {i} in seq2")
                break
        
        if not found and length <= 3:  # Only show short patterns that don't match
            formatted = finder.format_pattern(pattern)
            print(f"\nNO MATCH for: '{formatted}'")
            print(f"  Pattern from seq1: {pattern}")
            # Show what's at the corresponding positions in seq2
            for i in range(len(test7_seq2) - length + 1):
                seq2_slice = tuple(test7_seq2[i:i + length])
                print(f"  Seq2 at pos {i}: {seq2_slice}")

print("\n" + "="*60)
print("Key insight: The algorithm looks for EXACT tuple matches!")
print("="*60)

print("\nIn Test 7:")
print("  Seq1 has: ('quickly', 'ADVP')")
print("  Seq2 has: ('slowly', 'ADVP')")
print("  These have the same phrase type but different tokens!")

print("\nIn Test 8:")
print("  Seq1 has: ('very', 'ADJP')")
print("  Seq2 has: ('quite', 'ADJP')")
print("  Again, same phrase type but different tokens!")

# Let's verify this is the issue
print("\n" + "="*60)
print("Verification: What if the tokens were the same?")
print("="*60)

# Create modified sequences with matching tokens
test7_mod1 = [('Running', 'VP'), ('quickly', 'ADVP'), ('exhausted', 'VP'), ('him', 'NP'), ('completely', 'ADVP')]
test7_mod2 = [('Swimming', 'NP'), ('quickly', 'ADVP'), ('exhausted', 'VP'), ('him', 'NP'), ('completely', 'ADVP')]

print("\nModified Test 7 (same adverbs and pronouns):")
print(f"Mod1: {test7_mod1}")
print(f"Mod2: {test7_mod2}")

token_sequences = [("Text 1", test7_mod1), ("Text 2", test7_mod2)]
patterns = finder.find_common_patterns(token_sequences)

print(f"\nPatterns found: {len(patterns)}")
for pattern, count, num_files in patterns[:5]:
    formatted = finder.format_pattern(pattern)
    print(f"  '{formatted}' (count: {count})")

# The real issue
print("\n" + "="*60)
print("ROOT CAUSE ANALYSIS")
print("="*60)

print("\nThe PatternFinder at Level 3 looks for patterns where BOTH:")
print("1. The exact tokens match")
print("2. The phrase types match")
print("\nThis means 'quickly[ADVP]' does NOT match 'slowly[ADVP]'")
print("even though they have the same grammatical structure!")

print("\nFor the failed tests:")
print("\nTest 7: Different gerunds (Running/Swimming), adverbs (quickly/slowly),")
print("        verbs (exhausted/relaxed), pronouns (him/her), and adverbs (completely/totally)")
print("        Result: NO exact token matches → NO patterns found")

print("\nTest 8: Different pronouns (She/He), verbs (seems/looks),") 
print("        adverbs (very/quite), adjectives (happy/tired), and time words (today/now)")
print("        Result: NO exact token matches → NO patterns found")

print("\n" + "="*60)
print("CONCLUSION")
print("="*60)
print("\nThe algorithm is working as designed - it finds patterns where")
print("the EXACT SAME WORDS appear with the SAME PHRASE TYPES.")
print("\nTo find grammatical structure patterns (regardless of specific words),")
print("we would need a different analysis level that matches on phrase types alone.")