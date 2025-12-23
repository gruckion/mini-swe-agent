# Failure Analysis: django__django-15732

## Basic Info
```
{
  "exit_status": "Submitted",
  "api_calls": 31,
  "cost": 0.4518047999999999
}
```

## Token Usage
- Max prompt tokens: 21949

## Files Modified in Submission
```
- django/db/backends/base/schema.py
```

## Rule Violation Check

## Agent Reasoning About Tests
```
```

## Submission Diff (first 100 lines)
```diff
diff --git a/django/db/backends/base/schema.py b/django/db/backends/base/schema.py
index f2ca8c8df9..b3f9e7659a 100644
--- a/django/db/backends/base/schema.py
+++ b/django/db/backends/base/schema.py
@@ -528,7 +528,7 @@ class BaseDatabaseSchemaEditor:
         # Deleted uniques
         for fields in olds.difference(news):
             self._delete_composed_index(
-                model, fields, {"unique": True}, self.sql_delete_unique
+                model, fields, {"unique": True, "primary_key": False}, self.sql_delete_unique
             )
         # Created uniques
         for field_names in news.difference(olds):

```
