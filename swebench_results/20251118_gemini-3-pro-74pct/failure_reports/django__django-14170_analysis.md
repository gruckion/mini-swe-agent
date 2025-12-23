# Failure Analysis: django__django-14170

## Basic Info
```
{
  "exit_status": "Submitted",
  "api_calls": 39,
  "cost": 0.38302699999999995
}
```

## Token Usage
- Max prompt tokens: 22838

## Files Modified in Submission
```
- django/db/models/lookups.py
```

## Rule Violation Check

## Agent Reasoning About Tests
```
THOUGHT: I'm confident with the fix. I'll remove the temporary test files.
```

## Submission Diff (first 100 lines)
```diff
diff --git a/django/db/models/lookups.py b/django/db/models/lookups.py
index 916478d075..0ff7fef28b 100644
--- a/django/db/models/lookups.py
+++ b/django/db/models/lookups.py
@@ -550,6 +550,8 @@ class YearLookup(Lookup):
         # Avoid the extract operation if the rhs is a direct value to allow
         # indexes to be used.
         if self.rhs_is_direct_value():
+            if getattr(self.lhs, "lookup_name", None) == "iso_year":
+                return super().as_sql(compiler, connection)
             # Skip the extract part by directly using the originating field,
             # that is self.lhs.lhs.
             lhs_sql, params = self.process_lhs(compiler, connection, self.lhs.lhs)

```
