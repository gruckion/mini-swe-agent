# Failure Analysis: django__django-13512

## Basic Info
```
{
  "exit_status": "Submitted",
  "api_calls": 27,
  "cost": 0.2442818
}
```

## Token Usage
- Max prompt tokens: 15603

## Files Modified in Submission
```
- django/forms/fields.py
```

## Rule Violation Check

## Agent Reasoning About Tests
```
Now I should verify that `has_changed` works as expected. I'll create another test script for `has_changed`.
THOUGHT: Run the `has_changed` test.
4. Verified `has_changed` logic with a separate test script.
```

## Submission Diff (first 100 lines)
```diff
diff --git a/django/forms/fields.py b/django/forms/fields.py
index 9de2c60b35..6564db8586 100644
--- a/django/forms/fields.py
+++ b/django/forms/fields.py
@@ -1258,7 +1258,7 @@ class JSONField(CharField):
     def prepare_value(self, value):
         if isinstance(value, InvalidJSONInput):
             return value
-        return json.dumps(value, cls=self.encoder)
+        return json.dumps(value, ensure_ascii=False, cls=self.encoder)
 
     def has_changed(self, initial, data):
         if super().has_changed(initial, data):
@@ -1266,6 +1266,6 @@ class JSONField(CharField):
         # For purposes of seeing whether something has changed, True isn't the
         # same as 1 and the order of keys doesn't matter.
         return (
-            json.dumps(initial, sort_keys=True, cls=self.encoder) !=
-            json.dumps(self.to_python(data), sort_keys=True, cls=self.encoder)
+            json.dumps(initial, ensure_ascii=False, sort_keys=True, cls=self.encoder) !=
+            json.dumps(self.to_python(data), ensure_ascii=False, sort_keys=True, cls=self.encoder)
         )

```
