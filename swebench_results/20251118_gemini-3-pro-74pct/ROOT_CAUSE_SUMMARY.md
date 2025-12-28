# Root Cause Summary: 129 SWE-bench Failures

## Overview

This document summarizes the root causes for all 129 failed SWE-bench instances from the Gemini 3 Pro run (74.2% pass rate).

## High-Level Categorization

| Category | Count | % | Description |
|----------|-------|---|-------------|
| **Incorrect Fix Logic** | 95 | 73.6% | No rule violation, but fix was wrong |
| **Test Modifications** | 20 | 15.5% | Violated "don't modify tests" rule |
| **Config Modifications** | 17 | 13.2% | Violated "don't modify config" rule |

## Root Causes for "Incorrect Fix Logic" (95 instances)

### Summary by Specific Root Cause

| Root Cause | Count | % | Description |
|------------|-------|---|-------------|
| WRONG_API | 25 | 26.3% | Used incorrect attribute or method name |
| TYPE_MISMATCH | 21 | 22.1% | Incorrect types - wrong argument or return type |
| BEHAVIOR_MISMATCH | 21 | 22.1% | Fix behavior doesn't match expected test behavior |
| SUBTLE_LOGIC_ERROR | 8 | 8.4% | Small change but logic is incorrect |
| INCOMPLETE_FIX | 8 | 8.4% | Fix is incomplete - doesn't handle all cases |
| INDEX_ERROR | 4 | 4.2% | Array/list index out of bounds |
| MISSING_KEY | 4 | 4.2% | Fix doesn't handle all required dictionary keys |
| SYNTAX_ERROR | 2 | 2.1% | Fix has syntax errors |
| SCOPE_CREEP | 1 | 1.1% | Modified too many files |
| ERROR_HANDLING | 1 | 1.1% | Added error handling incorrectly |

### Key Insights

1. **70.5% of incorrect fixes are API/Type/Behavior issues**
   - WRONG_API (26.3%): Agent used wrong attribute/method names
   - TYPE_MISMATCH (22.1%): Wrong types for arguments or returns
   - BEHAVIOR_MISMATCH (22.1%): Fix doesn't match test expectations

2. **These are LSP-detectable issues**
   - WRONG_API → LSP can detect undefined attributes/methods
   - TYPE_MISMATCH → Type checker can catch type errors
   - Many could be prevented with static analysis

3. **Small fixes can still be wrong (8.4% SUBTLE_LOGIC_ERROR)**
   - Even minimal 1-2 line changes can have incorrect logic
   - Agent understood the problem but implementation was subtly wrong

4. **Scope creep is rare (1.1%)**
   - Most agents correctly focused on specific files
   - Over-engineering was not a major issue

## LSP-Detectable Error Analysis

Cross-referencing with our LSP analysis:

| Metric | Value |
|--------|-------|
| Failures with LSP-detectable runtime errors | 72.9% (94/129) |
| Errors appearing early (≤20% of session) | 58.5% |
| Cost spent in repair loops | 81.5% |
| Potential savings from early detection | $50.24 |

### Correlation

The high rate of WRONG_API (26.3%) and TYPE_MISMATCH (22.1%) failures correlates strongly with the 72.9% of failures that had LSP-detectable runtime errors (TypeError, AttributeError, etc.).

This validates the hypothesis that an LSP quality layer could prevent many of these failures by catching errors at edit time rather than runtime.

## Repository Breakdown

| Repository | Total Failures | No Violation | Test Mod | Config Mod |
|------------|---------------|--------------|----------|------------|
| django | 52 | 47 | 5 | 0 |
| sympy | 21 | 15 | 6 | 0 |
| sphinx | 14 | 3 | 1 | 11 |
| astropy | 9 | 3 | 3 | 6 |
| matplotlib | 9 | 8 | 1 | 0 |
| pylint | 8 | 5 | 2 | 0 |
| pytest | 4 | 2 | 2 | 0 |
| xarray | 4 | 4 | 0 | 0 |
| scikit-learn | 3 | 3 | 0 | 0 |
| requests | 3 | 3 | 0 | 0 |
| seaborn | 2 | 2 | 0 | 0 |

## Recommendations

### For AI Agent Improvement

1. **Add LSP validation layer** - Catch WRONG_API and TYPE_MISMATCH errors before submission
2. **Stricter type checking** - Use type hints and static analysis
3. **Better test understanding** - Parse tests to understand expected behavior
4. **Focused changes** - Avoid scope creep (though this was rare)

### For Policy Enforcement

1. **Strict test file blocking** - 15.5% of failures could be prevented
2. **Config file protection** - 13.2% of failures could be prevented
3. **Early validation** - Catch errors in first 20% of session

## Conclusion

The 95 "incorrect fix logic" failures break down into clear categories:
- **~70% are API/type/behavior mismatches** - potentially preventable with LSP tooling
- **~17% are logic errors** - harder to catch automatically
- **~13% are edge case/completeness issues** - need better test coverage analysis

Combined with the 37 rule violation failures (test/config modifications), approximately **50-60% of all failures** could potentially be prevented through:
1. Stricter policy enforcement (test/config protection)
2. LSP-based validation (API/type checking)
3. Early error detection (before repair loops consume budget)
