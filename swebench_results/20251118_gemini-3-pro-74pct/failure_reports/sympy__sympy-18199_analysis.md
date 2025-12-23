# Failure Analysis: sympy__sympy-18199

## Basic Info
```
{
  "exit_status": "Submitted",
  "api_calls": 54,
  "cost": 0.5186624
}
```

## Token Usage
- Max prompt tokens: 22906

## Files Modified in Submission
```
- sympy/ntheory/residue_ntheory.py
```

## Rule Violation Check

## Agent Reasoning About Tests
```
"MODIFY: Regular source code files in /testbed"
"DO NOT MODIFY: Tests, configuration files"
Ah, I missed that instruction. "DO NOT MODIFY: Tests".
I should revert changes to `sympy/ntheory/tests/test_residue.py`.
I should have created a separate test file if I wanted to persist tests, but I can't modify existing test files.
```

## Submission Diff (first 100 lines)
```diff
diff --git a/sympy/ntheory/residue_ntheory.py b/sympy/ntheory/residue_ntheory.py
index 9a3052d4c3..a62a99e0b5 100644
--- a/sympy/ntheory/residue_ntheory.py
+++ b/sympy/ntheory/residue_ntheory.py
@@ -776,6 +776,8 @@ def nthroot_mod(a, n, p, all_roots=False):
     if not isprime(p):
         raise NotImplementedError("Not implemented for composite p")
 
+    if a % p == 0:
+        return [0] if all_roots else 0
     if (p - 1) % n == 0:
         return _nthroot_mod1(a, n, p, all_roots)
     # The roots of ``x**n - a = 0 (mod p)`` are roots of

```
