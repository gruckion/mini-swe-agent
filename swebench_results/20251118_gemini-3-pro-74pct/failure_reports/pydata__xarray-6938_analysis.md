# Failure Analysis: pydata__xarray-6938

## Basic Info
```
{
  "exit_status": "Submitted",
  "api_calls": 34,
  "cost": 0.30986499999999995
}
```

## Token Usage
- Max prompt tokens: 17990

## Files Modified in Submission
```
- xarray/core/dataset.py
```

## Rule Violation Check

## Agent Reasoning About Tests
```
rm reproduce_issue.py apply_fix.py check_type.py check_coordinate_swap.py check_type_coord.py xarray/tests/test_swap_dims_mutation.py
THOUGHT: I removed the test file `xarray/tests/test_swap_dims_mutation.py`. I should probably keep it as part of the PR, so I will recreate it. The instructions say "MODIFY: Regular source code files in /testbed". It doesn't explicitly say I cannot add new test files, but usually I should add tests to existing test files or create new ones if appropriate. The instructions also say "DO NOT MODIFY: Tests", which implies I shouldn't change existing tests, but adding a new one might be discouraged if I'm supposed to only modify source code. However, usually adding a regression test is best practice.
Wait, "DO NOT MODIFY: Tests". This usually means "don't break existing tests or change them to pass incorrect code". It doesn't necessarily forbid adding new tests. But strictly speaking, if I add a file in `xarray/tests/`, I am modifying the `tests` directory.
"Your task is specifically to make changes to non-test files in the current directory in order to fix the issue described in the PR description in a way that is general and consistent with the codebase."
This phrasing suggests my primary task is the fix. However, verifying it with a test is part of the workflow.
```

## Submission Diff (first 100 lines)
```diff
diff --git a/xarray/core/dataset.py b/xarray/core/dataset.py
index c775d05c..27d16e1c 100644
--- a/xarray/core/dataset.py
+++ b/xarray/core/dataset.py
@@ -3773,6 +3773,8 @@ class Dataset(
             dims = tuple(dims_dict.get(dim, dim) for dim in v.dims)
             if k in result_dims:
                 var = v.to_index_variable()
+                if var is v:
+                    var = var.copy(deep=False)
                 var.dims = dims
                 if k in self._indexes:
                     indexes[k] = self._indexes[k]

```
