# Failure Analysis: django__django-11087

## Basic Info
```
{
  "exit_status": "Submitted",
  "api_calls": 44,
  "cost": 0.9866229999999998
}
```

## Token Usage
- Max prompt tokens: 59333

## Files Modified in Submission
```
- django/db/models/deletion.py
- update_deletion_debug.py
- update_deletion_final.py
```

## Rule Violation Check

## Agent Reasoning About Tests
```
Let's update `test_gfk.py`.
rm reproduce_issue.py check_parents.py check_only.py update_deletion.py test_parent_link.py test_gfk.py
This confirms that the fix works for the reported issue (assuming no signals) and doesn't break existing tests (which use signals).
```

## Submission Diff (first 100 lines)
```diff
diff --git a/django/db/models/deletion.py b/django/db/models/deletion.py
index 3a462f1c4c..a0ef413fd7 100644
--- a/django/db/models/deletion.py
+++ b/django/db/models/deletion.py
@@ -232,9 +232,15 @@ class Collector:
         """
         Get a QuerySet of objects related to `objs` via the relation `related`.
         """
-        return related.related_model._base_manager.using(self.using).filter(
+        qs = related.related_model._base_manager.using(self.using).filter(
             **{"%s__in" % related.field.name: objs}
         )
+        opts = related.related_model._meta
+        if (any(hasattr(f, "bulk_related_objects") for f in opts.private_fields) or
+                signals.pre_delete.has_listeners(related.related_model) or
+                signals.post_delete.has_listeners(related.related_model)):
+            return qs
+        return qs.only(opts.pk.name, *[f.name for f in opts.parents.values()])
 
     def instances_with_model(self):
         for model, instances in self.data.items():
diff --git a/update_deletion_debug.py b/update_deletion_debug.py
new file mode 100644
index 0000000000..6b8f114dc2
--- /dev/null
+++ b/update_deletion_debug.py
@@ -0,0 +1,16 @@
+import sys
+from django.db.models import signals
+
+file_path = 'django/db/models/deletion.py'
+with open(file_path, 'r') as f:
+    lines = f.readlines()
+
+# Find the line with opts = ...
+for i, line in enumerate(lines):
+    if 'opts = related.related_model._meta' in line:
+        # Insert print before it
+        lines.insert(i, '        print(f"Checking model {related.related_model}, has_pre: {signals.pre_delete.has_listeners(related.related_model)}, has_post: {signals.post_delete.has_listeners(related.related_model)}")\n')
+        break
+
+with open(file_path, 'w') as f:
+    f.writelines(lines)
diff --git a/update_deletion_final.py b/update_deletion_final.py
new file mode 100644
index 0000000000..a2e818b515
--- /dev/null
+++ b/update_deletion_final.py
@@ -0,0 +1,46 @@
+import sys
+
+file_path = 'django/db/models/deletion.py'
+with open(file_path, 'r') as f:
+    lines = f.readlines()
+
+# Find the related_objects method
+start_index = -1
+for i, line in enumerate(lines):
+    if 'def related_objects(self, related, objs):' in line:
+        start_index = i
+        break
+
+if start_index != -1:
+    # We want to replace the body of related_objects
+    # It spans from start_index to instances_with_model
+    end_index = -1
+    for i in range(start_index + 1, len(lines)):
+        if 'def instances_with_model(self):' in line: # Wait, line variable is stale loop var? No.
+            # Need to check lines[i]
+            pass
+        if 'def instances_with_model(self):' in lines[i]:
+            end_index = i
+            break
+    
+    if end_index != -1:
+        new_body = [
+            '    def related_objects(self, related, objs):\n',
+            '        """\n',
+            '        Get a QuerySet of objects related to `objs` via the relation `related`.\n',
+            '        """\n',
+            '        qs = related.related_model._base_manager.using(self.using).filter(\n',
+            '            **{"%s__in" % related.field.name: objs}\n',
+            '        )\n',
+            '        opts = related.related_model._meta\n',
+            '        if (any(hasattr(f, "bulk_related_objects") for f in opts.private_fields) or\n',
+            '                signals.pre_delete.has_listeners(related.related_model) or\n',
+            '                signals.post_delete.has_listeners(related.related_model)):\n',
+            '            return qs\n',
+            '        return qs.only(opts.pk.name, *[f.name for f in opts.parents.values()])\n',
+            '\n'
+        ]
+        lines[start_index:end_index] = new_body
+
+with open(file_path, 'w') as f:
+    f.writelines(lines)

```
