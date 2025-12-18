# Failure Analysis: sympy__sympy-20916

## Basic Info
```
{
  "exit_status": "Submitted",
  "api_calls": 51,
  "cost": 0.4833142499999999
}
```

## Token Usage
- Max prompt tokens: 25556

## Files Modified in Submission
```
- sympy/printing/conventions.py
- verify_split_super_sub.py
```

## Rule Violation Check

## Agent Reasoning About Tests
```
I should add a new test case for this issue in a new test file, or verify if I should modify existing tests. Instructions say "DO NOT MODIFY: Tests".
But I can create a new test file to verify my changes as part of my own process, but I should not commit it if I'm not supposed to modify tests.
"MODIFY: Regular source code files in /testbed ... DO NOT MODIFY: Tests".
This usually means don't change existing tests to make them pass if you broke them (unless the test was wrong).
But maybe I shouldn't add new tests to the repo if the instructions forbid modifying tests.
```

## Submission Diff (first 100 lines)
```diff
diff --git a/sympy/printing/conventions.py b/sympy/printing/conventions.py
index 9a3be6bbe9..5e3aa1ab54 100644
--- a/sympy/printing/conventions.py
+++ b/sympy/printing/conventions.py
@@ -7,7 +7,7 @@
 from collections.abc import Iterable
 from sympy import Derivative
 
-_name_with_digits_p = re.compile(r'^([a-zA-Z]+)([0-9]+)$')
+_name_with_digits_p = re.compile(r'^([^\W\d_]+)([0-9]+)$')
 
 
 def split_super_sub(text):
diff --git a/verify_split_super_sub.py b/verify_split_super_sub.py
new file mode 100644
index 0000000000..459a919206
--- /dev/null
+++ b/verify_split_super_sub.py
@@ -0,0 +1,17 @@
+from sympy.printing.conventions import split_super_sub
+
+# This was working before
+print(f"beta_13: {split_super_sub('beta_13')}") 
+
+# This relies on regex
+print(f"beta13: {split_super_sub('beta13')}") 
+
+# This relies on regex with unicode
+print(f"ω13: {split_super_sub('ω13')}") 
+
+# This should NOT split (mixed alpha numeric in name?)
+# If name is a1b2. split_super_sub regex expects [a-zA-Z]+[0-9]+. 
+# My regex [^\W\d_]+[0-9]+.
+# a1b2 -> [^\W\d_]+ matches 'a'. [0-9]+ matches '1'. Remaining 'b2'. Regex anchor $ fails.
+# So it shouldn't split.
+print(f"a1b2: {split_super_sub('a1b2')}")

```
