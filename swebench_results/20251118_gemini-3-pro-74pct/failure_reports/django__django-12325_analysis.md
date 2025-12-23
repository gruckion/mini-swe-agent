# Failure Analysis: django__django-12325

## Basic Info
```
{
  "exit_status": "Submitted",
  "api_calls": 35,
  "cost": 0.34437760000000006
}
```

## Token Usage
- Max prompt tokens: 21199

## Files Modified in Submission
```
- django/db/models/base.py
```

## Rule Violation Check

## Agent Reasoning About Tests
```
I'll modify `reproduce_issue.py` to test the other order as well.
I'll remove the newly created test file before submitting, as per instructions "DO NOT MODIFY: Tests". Wait, usually I should include regression tests. But the instructions say "DO NOT MODIFY: Tests". Does that mean existing tests or adding new tests?
"MODIFY: Regular source code files in /testbed"
"DO NOT MODIFY: Tests, configuration files"
Usually, adding a new test file is fine and encouraged, but modifying existing test files is restricted unless necessary. However, the instructions are quite specific. "Your task is specifically to make changes to non-test files in the current directory".
```

## Submission Diff (first 100 lines)
```diff
diff --git a/django/db/models/base.py b/django/db/models/base.py
index 8ea6c05ef9..7a8898b906 100644
--- a/django/db/models/base.py
+++ b/django/db/models/base.py
@@ -204,7 +204,12 @@ class ModelBase(type):
             for field in base._meta.local_fields:
                 if isinstance(field, OneToOneField):
                     related = resolve_relation(new_class, field.remote_field.model)
-                    parent_links[make_model_tuple(related)] = field
+                    related_key = make_model_tuple(related)
+                    if related_key in parent_links:
+                        prev_field = parent_links[related_key]
+                        if prev_field.remote_field.parent_link and not field.remote_field.parent_link:
+                            continue
+                    parent_links[related_key] = field
 
         # Track fields inherited from base models.
         inherited_attributes = set()

```
