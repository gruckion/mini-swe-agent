# Failure Analysis: django__django-14140

## Basic Info
```
{
  "exit_status": "Submitted",
  "api_calls": 25,
  "cost": 0.261538
}
```

## Token Usage
- Max prompt tokens: 16009

## Files Modified in Submission
```
- django/db/models/query_utils.py
```

## Rule Violation Check

## Agent Reasoning About Tests
```
I'll create a new test file `tests/queries/test_q_deconstruct_fix.py` instead of modifying the existing one, to keep things clean and avoid modifying existing tests if possible (though instructions say "DO NOT MODIFY: Tests", I can create new ones). Wait, instructions say "DO NOT MODIFY: Tests". Does that mean I cannot add new tests?
"DO NOT MODIFY: Tests, configuration files (pyproject.toml, setup.cfg, etc.)"
Usually this means I shouldn't change existing test logic to make my code pass if it's broken. But adding a reproduction test case is usually encouraged. However, the instructions are strict.
"Your task is specifically to make changes to non-test files in the current directory in order to fix the issue described in the PR description in a way that is general and consistent with the codebase."
```

## Submission Diff (first 100 lines)
```diff
diff --git a/django/db/models/query_utils.py b/django/db/models/query_utils.py
index ae0f886107..b8ae8d4b9c 100644
--- a/django/db/models/query_utils.py
+++ b/django/db/models/query_utils.py
@@ -85,7 +85,7 @@ class Q(tree.Node):
         if path.startswith('django.db.models.query_utils'):
             path = path.replace('django.db.models.query_utils', 'django.db.models')
         args, kwargs = (), {}
-        if len(self.children) == 1 and not isinstance(self.children[0], Q):
+        if len(self.children) == 1 and not isinstance(self.children[0], Q) and isinstance(self.children[0], tuple) and len(self.children[0]) == 2:
             child = self.children[0]
             kwargs = {child[0]: child[1]}
         else:

```
