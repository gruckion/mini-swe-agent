# Failure Report: mwaskom__seaborn-3187

**Labels:** `no-rule-violation`, `incorrect-fix-logic`

## Summary
Incorrect fix logic - changes don't pass original test suite

## Evidence

### Basic Info
- API Calls: 42
- Cost: $0.5055436
- Max Tokens: 24364

### Files Modified
```
- seaborn/_core/plot.py
- seaborn/_core/scales.py
```

### Agent Reasoning About Tests
The instruction says: "Your task is specifically to make changes to non-test files in the current directory in order to fix the issue described in the PR description in a way that is general and consistent with the codebase."

## Conclusion
**Failure Type:** Incorrect fix logic - changes don't pass original test suite
