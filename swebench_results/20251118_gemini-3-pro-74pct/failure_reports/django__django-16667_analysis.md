# Failure Analysis: django__django-16667

## Basic Info
```
{
  "exit_status": "Submitted",
  "api_calls": 19,
  "cost": 0.15340240000000002
}
```

## Token Usage
- Max prompt tokens: 13623

## Files Modified in Submission
```
- django/forms/widgets.py
```

## Rule Violation Check

## Agent Reasoning About Tests
```
THOUGHT: I'll create a new test file `tests/forms_tests/widget_tests/test_selectdatewidget_overflow.py` to avoid modifying the existing large test file too much and to keep my changes isolated. I'll copy the structure from `test_selectdatewidget.py`.
Wait, the instructions say "DO NOT MODIFY: Tests".
"MODIFY: Regular source code files in /testbed"
"DO NOT MODIFY: Tests, configuration files (pyproject.toml, setup.cfg, etc.)"
Ah, I missed that. I should NOT modify tests. I should only modify the source code.
```

## Submission Diff (first 100 lines)
```diff
diff --git a/django/forms/widgets.py b/django/forms/widgets.py
index 842b73e95c..f4bc74b7cd 100644
--- a/django/forms/widgets.py
+++ b/django/forms/widgets.py
@@ -1157,7 +1157,7 @@ class SelectDateWidget(Widget):
             input_format = formats.sanitize_strftime_format(input_format)
             try:
                 date_value = datetime.date(int(y), int(m), int(d))
-            except ValueError:
+            except (ValueError, OverflowError):
                 # Return pseudo-ISO dates with zeros for any unselected values,
                 # e.g. '2017-0-23'.
                 return "%s-%s-%s" % (y or 0, m or 0, d or 0)

```
