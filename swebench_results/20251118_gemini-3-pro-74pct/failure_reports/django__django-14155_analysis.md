# Failure Analysis: django__django-14155

## Basic Info
```
{
  "exit_status": "Submitted",
  "api_calls": 22,
  "cost": 0.321335
}
```

## Token Usage
- Max prompt tokens: 20281

## Files Modified in Submission
```
- django/urls/resolvers.py
```

## Rule Violation Check

## Agent Reasoning About Tests
```
I verified the fix with a reproduction script and new tests.
THOUGHT: I should probably keep the test file as part of the PR, but the instructions say "MODIFY: Regular source code files in /testbed ... DO NOT MODIFY: Tests".
Wait, "DO NOT MODIFY: Tests" usually means don't change existing tests to make them pass if they are broken by your changes (unless the test is wrong).
However, the instructions say "DO NOT MODIFY: Tests".
"Your task is specifically to make changes to non-test files in the current directory in order to fix the issue described in the PR description".
```

## Submission Diff (first 100 lines)
```diff
diff --git a/django/urls/resolvers.py b/django/urls/resolvers.py
index 9b00e24509..7d7c84f027 100644
--- a/django/urls/resolvers.py
+++ b/django/urls/resolvers.py
@@ -31,6 +31,10 @@ from .utils import get_callable
 
 class ResolverMatch:
     def __init__(self, func, args, kwargs, url_name=None, app_names=None, namespaces=None, route=None, tried=None):
+        while isinstance(func, functools.partial):
+            args = func.args + tuple(args)
+            kwargs = {**func.keywords, **kwargs}
+            func = func.func
         self.func = func
         self.args = args
         self.kwargs = kwargs

```
