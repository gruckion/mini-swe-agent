# Failure Analysis: django__django-15503

## Basic Info
```
{
  "exit_status": "Submitted",
  "api_calls": 27,
  "cost": 0.518877
}
```

## Token Usage
- Max prompt tokens: 29708

## Files Modified in Submission
```
- django/db/models/fields/json.py
```

## Rule Violation Check

## Agent Reasoning About Tests
```
rm reproduce_issue.py test_json_path.py apply_fix.py test_edge_cases.py test_key_transform_rhs.py
```

## Submission Diff (first 100 lines)
```diff
diff --git a/django/db/models/fields/json.py b/django/db/models/fields/json.py
index fdca700c9d..a36bc2ba81 100644
--- a/django/db/models/fields/json.py
+++ b/django/db/models/fields/json.py
@@ -191,16 +191,19 @@ class HasKeyLookup(PostgresOperatorLookup):
         for key in rhs:
             if isinstance(key, KeyTransform):
                 *_, rhs_key_transforms = key.preprocess_lhs(compiler, connection)
+                rhs_json_path = compile_json_path(rhs_key_transforms, include_root=False)
             else:
-                rhs_key_transforms = [key]
+                if isinstance(key, int):
+                    rhs_json_path = compile_json_path([key], include_root=False)
+                else:
+                    rhs_json_path = '.' + json.dumps(key)
             rhs_params.append(
-                "%s%s"
+                '%s%s'
                 % (
                     lhs_json_path,
-                    compile_json_path(rhs_key_transforms, include_root=False),
+                    rhs_json_path,
                 )
             )
-        # Add condition for each key.
         if self.logical_operator:
             sql = "(%s)" % self.logical_operator.join([sql] * len(rhs_params))
         return sql, tuple(lhs_params) + tuple(rhs_params)

```
