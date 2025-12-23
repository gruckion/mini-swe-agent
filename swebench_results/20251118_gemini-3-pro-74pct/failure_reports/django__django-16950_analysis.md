# Failure Analysis: django__django-16950

## Basic Info
```
{
  "exit_status": "Submitted",
  "api_calls": 86,
  "cost": 1.5578134000000001
}
```

## Token Usage
- Max prompt tokens: 68943

## Files Modified in Submission
```
- django/forms/models.py
```

## Rule Violation Check

## Agent Reasoning About Tests
```
I'll modify `reproduce_issue.py` to test this hypothesis instead of creating a new file, or just append to it.
I have fixed the issue and verified it with a reproduction script, and ensured that existing tests pass.
```

## Submission Diff (first 100 lines)
```diff
diff --git a/django/forms/models.py b/django/forms/models.py
index 3fa04b821f..819558f8b2 100644
--- a/django/forms/models.py
+++ b/django/forms/models.py
@@ -1177,7 +1177,7 @@ class BaseInlineFormSet(BaseModelFormSet):
                 to_field = self.instance._meta.get_field(kwargs["to_field"])
             else:
                 to_field = self.instance._meta.pk
-            if to_field.has_default():
+            if to_field.has_default() and getattr(self.instance, to_field.attname) is None:
                 setattr(self.instance, to_field.attname, None)
 
         form.fields[name] = InlineForeignKeyField(self.instance, **kwargs)

```
