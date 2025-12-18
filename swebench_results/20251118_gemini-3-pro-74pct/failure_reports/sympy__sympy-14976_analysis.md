# Failure Analysis: sympy__sympy-14976

## Basic Info
```
{
  "exit_status": "Submitted",
  "api_calls": 41,
  "cost": 0.3726218
}
```

## Token Usage
- Max prompt tokens: 22979

## Files Modified in Submission
```
- sympy/printing/pycode.py
```

## Rule Violation Check

## Agent Reasoning About Tests
```
I'll create a new test file `sympy/utilities/tests/test_lambdify_mpmath_rational.py` to ensure this fix is preserved in the future. Wait, I am not allowed to modify tests or create new test files in the codebase permanently if they are not part of the PR. But I can create a test file to verify my changes and then delete it, or if I am supposed to add a regression test.
"MODIFY: Regular source code files in /testbed"
"DO NOT MODIFY: Tests, configuration files"
```

## Submission Diff (first 100 lines)
```diff
diff --git a/sympy/printing/pycode.py b/sympy/printing/pycode.py
index d06901425d..a5278c353d 100644
--- a/sympy/printing/pycode.py
+++ b/sympy/printing/pycode.py
@@ -331,6 +331,11 @@ def _print_Float(self, e):
         args = str(tuple(map(int, e._mpf_)))
         return '{func}({args})'.format(func=self._module_format('mpmath.mpf'), args=args)
 
+    def _print_Rational(self, e):
+        return "{func}('{val}')".format(
+            func=self._module_format('mpmath.mpf'),
+            val=str(e))
+
 
     def _print_uppergamma(self, e):
         return "{0}({1}, {2}, {3})".format(

```
