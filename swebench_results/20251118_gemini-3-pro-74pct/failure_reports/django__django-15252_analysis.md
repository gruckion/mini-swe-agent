# Failure Analysis: django__django-15252

## Basic Info
```
{
  "exit_status": "Submitted",
  "api_calls": 22,
  "cost": 0.3238773999999999
}
```

## Token Usage
- Max prompt tokens: 19716

## Files Modified in Submission
```
- django/db/migrations/recorder.py
```

## Rule Violation Check

## Agent Reasoning About Tests
```
I'll modify the reproduction script to test `record_applied`.
```

## Submission Diff (first 100 lines)
```diff
diff --git a/django/db/migrations/recorder.py b/django/db/migrations/recorder.py
index 1a37c6b7d0..e149a6daab 100644
--- a/django/db/migrations/recorder.py
+++ b/django/db/migrations/recorder.py
@@ -1,5 +1,5 @@
 from django.apps.registry import Apps
-from django.db import DatabaseError, models
+from django.db import DatabaseError, models, router
 from django.utils.functional import classproperty
 from django.utils.timezone import now
 
@@ -62,6 +62,9 @@ class MigrationRecorder:
         # in the codebase.
         if self.has_table():
             return
+        # Check if the router allows this model to be migrated to this database
+        if not router.allow_migrate_model(self.connection.alias, self.Migration):
+            return
         # Make the table
         try:
             with self.connection.schema_editor() as editor:
@@ -84,13 +87,26 @@ class MigrationRecorder:
     def record_applied(self, app, name):
         """Record that a migration was applied."""
         self.ensure_schema()
-        self.migration_qs.create(app=app, name=name)
+        try:
+            self.migration_qs.create(app=app, name=name)
+        except DatabaseError:
+            # The table might be missing because the router disallowed its creation.
+            if not self.has_table():
+                return
+            raise
 
     def record_unapplied(self, app, name):
         """Record that a migration was unapplied."""
         self.ensure_schema()
-        self.migration_qs.filter(app=app, name=name).delete()
+        try:
+            self.migration_qs.filter(app=app, name=name).delete()
+        except DatabaseError:
+            # The table might be missing because the router disallowed its creation.
+            if not self.has_table():
+                return
+            raise
 
     def flush(self):
         """Delete all migration records. Useful for testing migrations."""
-        self.migration_qs.all().delete()
+        if self.has_table():
+            self.migration_qs.all().delete()

```
