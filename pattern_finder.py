#!/usr/bin/env python3
import os
import sys
import glob
from collections import defaultdict
import argparse
import spacy

class PatternFinder:
    def __init__(self, level=1):
        self.level = level
        self.nlp = None
        if level > 1:
            try:
                self.nlp = spacy.load('en_core_web_sm')
            except:
                print("Please install spacy and en_core_web_sm: python -m spacy download en_core_web_sm")
                sys.exit(1)
    
    def get_files_from_folder(self, folder):
        """Get all text files from a folder"""
        pattern = os.path.join(folder, '*.txt')
        files = glob.glob(pattern)
        if not files:
            print(f"No text files found in {folder}")
            sys.exit(1)
        return files
    
    def read_texts(self, files):
        """Read all text files"""
        texts = []
        for file_path in files:
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read().strip()
                    if content:
                        texts.append((file_path, content))
            except Exception as e:
                print(f"Error reading {file_path}: {e}")
        return texts
    
    def tokenize(self, text):
        """Tokenize text based on level"""
        if self.level == 1:
            # Simple token level
            if self.nlp:
                doc = self.nlp(text)
                return [token.text for token in doc if not token.is_space]
            else:
                # Fallback to simple split
                return text.split()
        
        elif self.level == 2:
            # Token + POS
            doc = self.nlp(text)
            return [(token.text, token.pos_) for token in doc if not token.is_space]
        
        elif self.level == 3:
            # Token + phrase
            doc = self.nlp(text)
            tokens = []
            for token in doc:
                if token.is_space:
                    continue
                phrase_type = self.get_phrase_type(token, doc)
                tokens.append((token.text, phrase_type))
            return tokens
        
        elif self.level == 4:
            # Token + POS + phrase
            doc = self.nlp(text)
            tokens = []
            for token in doc:
                if token.is_space:
                    continue
                phrase_type = self.get_phrase_type(token, doc)
                tokens.append((token.text, token.pos_, phrase_type))
            return tokens
    
    def get_phrase_type(self, token, doc):
        """Get phrase type for a token"""
        # Check if token is part of a noun chunk
        for chunk in doc.noun_chunks:
            if token.i >= chunk.start and token.i < chunk.end:
                return 'NP'
        
        # Check for verb phrase (simple heuristic)
        if token.pos_ in ['VERB', 'AUX']:
            return 'VP'
        
        # Check for prepositional phrase
        if token.pos_ == 'ADP' or token.dep_ == 'prep':
            return 'PP'
        
        # Check for adjective phrase
        if token.pos_ == 'ADJ':
            return 'ADJP'
        
        # Check for adverb phrase
        if token.pos_ == 'ADV':
            return 'ADVP'
        
        return 'O'  # Other
    
    def find_common_patterns(self, token_sequences):
        """Find all common patterns across sequences"""
        if len(token_sequences) < 2:
            print("Need at least 2 texts to find common patterns")
            return []
        
        # Find all patterns
        patterns = defaultdict(lambda: {'count': 0, 'files': set()})
        
        # Use the shortest sequence as base
        base_idx = min(range(len(token_sequences)), key=lambda i: len(token_sequences[i][1]))
        base_file, base_seq = token_sequences[base_idx]
        
        # Try all possible substrings from the base sequence
        n = len(base_seq)
        for length in range(n, 0, -1):
            for start in range(n - length + 1):
                pattern = tuple(base_seq[start:start + length])
                
                # Check if this pattern exists in all other sequences
                found_in_all = True
                total_count = 0
                files_with_pattern = set()
                
                for file_path, seq in token_sequences:
                    count = self.count_pattern_in_sequence(pattern, seq)
                    if count > 0:
                        total_count += count
                        files_with_pattern.add(file_path)
                    else:
                        found_in_all = False
                
                # Only include patterns found in at least 2 files
                if len(files_with_pattern) >= 2:
                    patterns[pattern]['count'] = total_count
                    patterns[pattern]['files'] = files_with_pattern
        
        # Convert to list and sort by length (longest first), then by count
        result = []
        for pattern, info in patterns.items():
            result.append((pattern, info['count'], len(info['files'])))
        
        result.sort(key=lambda x: (len(x[0]), x[1], x[2]), reverse=True)
        return result
    
    def count_pattern_in_sequence(self, pattern, sequence):
        """Count occurrences of pattern in sequence"""
        count = 0
        pattern_len = len(pattern)
        seq_len = len(sequence)
        
        for i in range(seq_len - pattern_len + 1):
            if tuple(sequence[i:i + pattern_len]) == pattern:
                count += 1
        
        return count
    
    def format_pattern(self, pattern):
        """Format pattern for display"""
        if self.level == 1:
            return ' '.join(pattern)
        elif self.level == 2:
            return ' '.join([f"{token}({pos})" for token, pos in pattern])
        elif self.level == 3:
            return ' '.join([f"{token}[{phrase}]" for token, phrase in pattern])
        elif self.level == 4:
            return ' '.join([f"{token}({pos})[{phrase}]" for token, pos, phrase in pattern])
    
    def run(self, folder_path):
        """Main execution"""
        # Get files
        files = self.get_files_from_folder(folder_path)
        print(f"Found {len(files)} text file(s) in {folder_path}")
        
        # Read and tokenize texts
        texts = self.read_texts(files)
        if len(texts) < 2:
            print("Need at least 2 texts with content to find patterns")
            return
        
        print(f"Processing {len(texts)} text(s)...")
        
        # Tokenize each text
        token_sequences = []
        for file_path, text in texts:
            tokens = self.tokenize(text)
            if tokens:
                token_sequences.append((file_path, tokens))
                print(f"  - {os.path.basename(file_path)}: {len(tokens)} tokens")
        
        # Find common patterns
        print(f"\nFinding common patterns (Level {self.level})...")
        patterns = self.find_common_patterns(token_sequences)
        
        # Display results
        print(f"\nFound {len(patterns)} common patterns:\n")
        
        if not patterns:
            print("No common patterns found.")
            return
        
        # Show top patterns
        max_display = min(20, len(patterns))
        for i, (pattern, count, num_files) in enumerate(patterns[:max_display], 1):
            formatted = self.format_pattern(pattern)
            print(f"{i}. Pattern: \"{formatted}\"")
            print(f"   Length: {len(pattern)} tokens")
            print(f"   Total occurrences: {count}")
            print(f"   Found in {num_files} file(s)")
            print()
        
        if len(patterns) > max_display:
            print(f"... and {len(patterns) - max_display} more patterns")


def main():
    parser = argparse.ArgumentParser(description='Find longest shared patterns in text files')
    parser.add_argument('folder', help='Folder containing text files')
    parser.add_argument('--level', type=int, default=1, choices=[1, 2, 3, 4],
                        help='Analysis level: 1=token, 2=token+POS, 3=token+phrase, 4=token+POS+phrase')
    
    args = parser.parse_args()
    
    # Create pattern finder
    finder = PatternFinder(level=args.level)
    
    # Run analysis
    finder.run(args.folder)


if __name__ == '__main__':
    main()