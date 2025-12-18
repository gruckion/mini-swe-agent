# Failure Analysis: django__django-11477

## Basic Info
```
{
  "exit_status": "Submitted",
  "api_calls": 33,
  "cost": 0.3263359999999999
}
```

## Token Usage
- Max prompt tokens: 22400

## Files Modified in Submission
```
- django/urls/base.py
```

## Rule Violation Check

## Agent Reasoning About Tests
```
I'll update the test expectation to match what `reverse` produces.
I'll update `tests/i18n/patterns/tests.py` with the corrected expectations.
"MODIFY: Regular source code files in /testbed"
"DO NOT MODIFY: Tests, configuration files"
Wait, "DO NOT MODIFY: Tests".
```

## Submission Diff (first 100 lines)
```diff
diff --git a/django/urls/base.py b/django/urls/base.py
index 0e1c3d909c..2ce0bc53fc 100644
--- a/django/urls/base.py
+++ b/django/urls/base.py
@@ -172,7 +172,11 @@ def translate_url(url, lang_code):
         to_be_reversed = "%s:%s" % (match.namespace, match.url_name) if match.namespace else match.url_name
         with override(lang_code):
             try:
-                url = reverse(to_be_reversed, args=match.args, kwargs=match.kwargs)
+                url = reverse(
+                    to_be_reversed,
+                    args=[arg for arg in match.args if arg is not None],
+                    kwargs={k: v for k, v in match.kwargs.items() if v is not None},
+                )
             except NoReverseMatch:
                 pass
             else:

```
