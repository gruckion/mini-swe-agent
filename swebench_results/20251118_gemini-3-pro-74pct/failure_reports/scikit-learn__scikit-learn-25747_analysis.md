# Failure Analysis: scikit-learn__scikit-learn-25747

## Basic Info
```
{
  "exit_status": "Submitted",
  "api_calls": 31,
  "cost": 0.5516483999999999
}
```

## Token Usage
- Max prompt tokens: 34914

## Files Modified in Submission
```
- sklearn/utils/_set_output.py
```

## Rule Violation Check

## Agent Reasoning About Tests
```
THOUGHT: I should also remove the new test from `sklearn/utils/tests/test_set_output.py` because I am not supposed to modify test files?
"MODIFY: Regular source code files in /testbed (this is the working directory for all your subsequent commands)"
"DO NOT MODIFY: Tests, configuration files (pyproject.toml, setup.cfg, etc.)"
THOUGHT: I verified my fix with the test I added (and then reverted). The fix is in `sklearn/utils/_set_output.py`.
```

## Submission Diff (first 100 lines)
```diff
diff --git a/sklearn/utils/_set_output.py b/sklearn/utils/_set_output.py
index 335773c6a..f96a0fc67 100644
--- a/sklearn/utils/_set_output.py
+++ b/sklearn/utils/_set_output.py
@@ -55,10 +55,13 @@ def _wrap_in_pandas_container(
     if isinstance(data_to_wrap, pd.DataFrame):
         if columns is not None:
             data_to_wrap.columns = columns
-        if index is not None:
+        if index is not None and len(index) == len(data_to_wrap):
             data_to_wrap.index = index
         return data_to_wrap
 
+    if index is not None and len(index) != len(data_to_wrap):
+        index = None
+
     return pd.DataFrame(data_to_wrap, index=index, columns=columns)
 
 

```
