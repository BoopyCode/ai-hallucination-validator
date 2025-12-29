#!/usr/bin/env python3
"""
AI Hallucination Validator - Because your AI assistant might be high on training data.
Checks if code contains imaginary libraries, deprecated methods, or fantasy APIs.
"""

import ast
import sys
import re
from typing import List, Dict

# Known imaginary libraries that AIs love to invent
IMAGINARY_LIBS = {
    'neuralnet': "That's not a library, that's a concept",
    'deeplearn': "Sounds cool, doesn't exist",
    'aiutils': "AI made this up while dreaming",
    'tensorflow2': "There's only tensorflow, and you're not using it",
    'pytorch_light': "You mean lightning? Or just wishful thinking?",
    'sklearn2': "Scikit-learn didn't get the memo about version 2",
    'opencv5': "We're still at 4, time traveler",
    'fastai3': "FastAI is already fast, no need for version 3"
}

# Deprecated methods that haunt old tutorials
DEPRECATED_PATTERNS = [
    (r'\.fit_transform\(X, y\)', "fit_transform doesn't take y - your AI is remembering wrong"),
    (r'from sklearn\.cross_validation import', "cross_validation died in 2017, RIP"),
    (r'pd\.rolling_mean', "Pandas buried this in 2018"),
    (r'tf\.Session\(\)', "TensorFlow 2 called, they want their sessions back")
]

def analyze_code(code: str) -> Dict[str, List[str]]:
    """
    Analyzes code for AI hallucinations.
    Returns findings that would make a real developer cry.
    """
    findings = {"imaginary_libs": [], "deprecated": [], "suspicious": []}
    
    # Check for import statements
    try:
        tree = ast.parse(code)
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for alias in node.names:
                    lib = alias.name.split('.')[0]
                    if lib in IMAGINARY_LIBS:
                        findings["imaginary_libs"].append(
                            f"'{lib}' - {IMAGINARY_LIBS[lib]}"
                        )
            elif isinstance(node, ast.ImportFrom):
                if node.module:
                    lib = node.module.split('.')[0]
                    if lib in IMAGINARY_LIBS:
                        findings["imaginary_libs"].append(
                            f"'{lib}' - {IMAGINARY_LIBS[lib]}"
                        )
    except SyntaxError:
        findings["suspicious"].append("Code won't even parse - AI might be drunk")
    
    # Check for deprecated patterns
    for pattern, message in DEPRECATED_PATTERNS:
        if re.search(pattern, code):
            findings["deprecated"].append(message)
    
    # Bonus: Check for suspiciously perfect variable names
    if 'perfect_model' in code or 'final_solution' in code:
        findings["suspicious"].append("Variable names too optimistic - classic AI overconfidence")
    
    return findings

def main():
    """Main function that judges AI-generated code."""
    if len(sys.argv) != 2:
        print("Usage: python hallucination_validator.py <filename>")
        print("Example: python hallucination_validator.py suspicious_ai_code.py")
        sys.exit(1)
    
    filename = sys.argv[1]
    try:
        with open(filename, 'r') as f:
            code = f.read()
    except FileNotFoundError:
        print(f"File '{filename}' not found. Did your AI imagine this too?")
        sys.exit(1)
    
    findings = analyze_code(code)
    
    print(f"\n🔍 Analyzing: {filename}")
    print("=" * 50)
    
    if not any(findings.values()):
        print("✅ Code looks plausible! (Or the AI is getting smarter...)")
        return
    
    print("🚨 AI HALLUCINATIONS DETECTED!\n")
    
    for category, items in findings.items():
        if items:
            print(f"{category.replace('_', ' ').title()}:")
            for item in items:
                print(f"  • {item}")
            print()
    
    print("💡 Tip: Your AI might need less sci-fi and more documentation")

if __name__ == "__main__":
    main()
