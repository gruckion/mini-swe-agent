# Failure Analysis: sympy__sympy-15875

## Basic Info
```
{
  "exit_status": "Submitted",
  "api_calls": 27,
  "cost": 0.4208726
}
```

## Token Usage
- Max prompt tokens: 23416

## Files Modified in Submission
```
- sympy/core/add.py
```

## Rule Violation Check

## Agent Reasoning About Tests
```
rm reproduce_issue.py check_args.py check_zero_imaginary.py update_add.py check_is_zero.py check_real.py check_eval_is_zero.py test_fix.py
THOUGHT: I have fixed the issue in `sympy/core/add.py` and verified it with reproduction script and existing tests.
```

## Submission Diff (first 100 lines)
```diff
diff --git a/sympy/core/add.py b/sympy/core/add.py
index 83a5f2aedc..3ddaf089ec 100644
--- a/sympy/core/add.py
+++ b/sympy/core/add.py
@@ -534,37 +534,43 @@ def _eval_is_zero(self):
             # issue 10528: there is no way to know if a nc symbol
             # is zero or not
             return
-        nz = []
-        z = 0
-        im_or_z = False
-        im = False
+
+        reals = []
+        imaginaries = []
+
         for a in self.args:
             if a.is_real:
                 if a.is_zero:
-                    z += 1
-                elif a.is_zero is False:
-                    nz.append(a)
+                    continue
+                if a.is_zero is False:
+                    reals.append(a)
                 else:
                     return
-            elif a.is_imaginary:
-                im = True
-            elif (S.ImaginaryUnit*a).is_real:
-                im_or_z = True
+            elif a.is_imaginary or (S.ImaginaryUnit*a).is_real:
+                if a.is_zero:
+                    continue
+                imaginaries.append(a)
             else:
                 return
-        if z == len(self.args):
-            return True
-        if len(nz) == len(self.args):
-            return None
-        b = self.func(*nz)
-        if b.is_zero:
-            if not im_or_z and not im:
-                return True
-            if im and not im_or_z:
-                return False
-        if b.is_zero is False:
+
+        if not imaginaries:
+            if len(reals) == len(self.args):
+                return None
+            return self.func(*reals).is_zero
+
+        r_sum = self.func(*reals)
+        if r_sum.is_zero is False:
             return False
 
+        i_sum = self.func(*[i/S.ImaginaryUnit for i in imaginaries])
+        if i_sum.is_zero is False:
+            return False
+
+        if r_sum.is_zero and i_sum.is_zero:
+            return True
+
+        return None
+
     def _eval_is_odd(self):
         l = [f for f in self.args if not (f.is_even is True)]
         if not l:

```
