# Failure Analysis: sympy__sympy-17318

## Basic Info
```
{
  "exit_status": "Submitted",
  "api_calls": 35,
  "cost": 0.3950005999999999
}
```

## Token Usage
- Max prompt tokens: 24288

## Files Modified in Submission
```
- sympy/simplify/radsimp.py
- sympy/simplify/tests/test_sqrtdenest.py
```

## Rule Violation Check
### ❌ TEST FILES MODIFIED
```
diff --git a/sympy/simplify/tests/test_sqrtdenest.py b/sympy/simplify/tests/test_sqrtdenest.py
--- a/sympy/simplify/tests/test_sqrtdenest.py
+++ b/sympy/simplify/tests/test_sqrtdenest.py
```

## Agent Reasoning About Tests
```
I have verified the fix with a reproduction script and added a regression test.
```

## Submission Diff (first 100 lines)
```diff
diff --git a/sympy/simplify/radsimp.py b/sympy/simplify/radsimp.py
index 216ae26204..de59422669 100644
--- a/sympy/simplify/radsimp.py
+++ b/sympy/simplify/radsimp.py
@@ -1113,6 +1113,8 @@ def _split_gcd(*a):
     >>> _split_gcd(55, 35, 22, 14, 77, 10)
     (5, [55, 35, 10], [22, 14, 77])
     """
+    if not a:
+        return 1, [], []
     g = a[0]
     b1 = [g]
     b2 = []
diff --git a/sympy/simplify/tests/test_sqrtdenest.py b/sympy/simplify/tests/test_sqrtdenest.py
index c30f7a3235..247ec72da2 100644
--- a/sympy/simplify/tests/test_sqrtdenest.py
+++ b/sympy/simplify/tests/test_sqrtdenest.py
@@ -183,3 +183,17 @@ def test_issue_5653():
 
 def test_sqrt_ratcomb():
     assert sqrtdenest(sqrt(1 + r3) + sqrt(3 + 3*r3) - sqrt(10 + 6*r3)) == 0
+
+def test_issue_12420():
+    from sympy import I
+    # This should not raise IndexError
+    e = (3 - sqrt(2)*sqrt(4 + 3*I) + 3*I)/2
+    assert sqrtdenest(e) == I
+    # Also test with evaluate=False to ensure it doesn't crash if not simplified
+    from sympy import Mul, Add, Integer
+    e2 = Mul(S.Half, Add(Integer(3), Mul(Integer(3), I), Mul(Integer(-1), sqrt(2), sqrt(Add(Integer(4), Mul(Integer(3), I), evaluate=False)), evaluate=False), evaluate=False), evaluate=False)
+    # If it cannot be denested, it should be returned unchanged (or slightly simplified)
+    # But in this case, it CAN be denested to I if simplified.
+    # If we pass it to sqrtdenest, it might simplify it.
+    # The important thing is that it doesn't raise IndexError.
+    sqrtdenest(e2)

```
