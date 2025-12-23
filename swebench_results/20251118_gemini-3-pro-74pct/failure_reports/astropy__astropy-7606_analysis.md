# Failure Analysis: astropy__astropy-7606

## Basic Info
```
{
  "exit_status": "Submitted",
  "api_calls": 31,
  "cost": 0.22861220000000002
}
```

## Token Usage
- Max prompt tokens: 13125

## Files Modified in Submission
```
- astropy/units/core.py
```

## Rule Violation Check

## Agent Reasoning About Tests
```
rm reproduce_issue.py test_fix.py test_is_equivalent.py test_unrecognized_is_equivalent.py test_unitbase_eq.py
```

## Submission Diff (first 100 lines)
```diff
diff --git a/astropy/units/core.py b/astropy/units/core.py
index e9bd986d33..4f0316cc06 100644
--- a/astropy/units/core.py
+++ b/astropy/units/core.py
@@ -1710,7 +1710,10 @@ class UnrecognizedUnit(IrreducibleUnit):
         _unrecognized_operator
 
     def __eq__(self, other):
-        other = Unit(other, parse_strict='silent')
+        try:
+            other = Unit(other, parse_strict="silent")
+        except (ValueError, UnitsError, TypeError):
+            return False
         return isinstance(other, UnrecognizedUnit) and self.name == other.name
 
     def __ne__(self, other):

```
