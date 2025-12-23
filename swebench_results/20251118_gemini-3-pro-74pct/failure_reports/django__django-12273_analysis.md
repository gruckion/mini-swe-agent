# Failure Analysis: django__django-12273

## Basic Info
```
{
  "exit_status": "Submitted",
  "api_calls": 33,
  "cost": 0.5803891999999999
}
```

## Token Usage
- Max prompt tokens: 31750

## Files Modified in Submission
```
- django/db/models/base.py
```

## Rule Violation Check

## Agent Reasoning About Tests
```
Or, I can just use `SchemaEditor` to create the tables manually in `setUp` or `setUpClass` of the test case, bypassing the automatic test database creation's migration step (which might be failing to see the models).
Let's try to fix the reproduction script by ensuring tables are created. I'll modify the script to explicitly create tables using `call_command('migrate', run_syncdb=True)` inside the test runner setup or just use `SchemaEditor`.
I'll modify the script to print registered models before running tests.
Let's update the test case.
```

## Submission Diff (first 100 lines)
```diff
diff --git a/django/db/models/base.py b/django/db/models/base.py
index 844c01e95e..2800410ff3 100644
--- a/django/db/models/base.py
+++ b/django/db/models/base.py
@@ -806,7 +806,10 @@ class Model(metaclass=ModelBase):
             # Make sure the link fields are synced between parent and self.
             if (field and getattr(self, parent._meta.pk.attname) is None and
                     getattr(self, field.attname) is not None):
-                setattr(self, parent._meta.pk.attname, getattr(self, field.attname))
+                if not self._state.adding:
+                    setattr(self, field.attname, None)
+                else:
+                    setattr(self, parent._meta.pk.attname, getattr(self, field.attname))
             parent_inserted = self._save_parents(cls=parent, using=using, update_fields=update_fields)
             updated = self._save_table(
                 cls=parent, using=using, update_fields=update_fields,

```
