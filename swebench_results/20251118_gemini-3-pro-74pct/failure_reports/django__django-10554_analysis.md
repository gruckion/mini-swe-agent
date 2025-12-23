# Failure Analysis: django__django-10554

## Basic Info
```
{
  "exit_status": "Submitted",
  "api_calls": 43,
  "cost": 0.5601662000000001
}
```

## Token Usage
- Max prompt tokens: 31273

## Files Modified in Submission
```
- django/db/models/sql/compiler.py
```

## Rule Violation Check

## Agent Reasoning About Tests
```
THOUGHT: Ah, `migrate` command doesn't work well with `__main__` app defined in the same script without proper setup. I should use `makemigrations` and `migrate` or just `SchemaEditor` to create the table manually. Or I can use `django.test.utils.setup_test_environment`?
To verify if this fixes the issue, I would ideally need a test case that fails before and passes after. Since I can't fully reproduce the failure on SQLite (due to syntax error masking the corruption or lack of corruption visibility), I have to rely on the logic that `as_sql` mutates the query and `combined_queries` are shared, so cloning is necessary.
THOUGHT: Now that I've applied the fix, I should verify that it doesn't break existing tests.
```

## Submission Diff (first 100 lines)
```diff
diff --git a/django/db/models/sql/compiler.py b/django/db/models/sql/compiler.py
index a791908caf..a5158b93be 100644
--- a/django/db/models/sql/compiler.py
+++ b/django/db/models/sql/compiler.py
@@ -410,7 +410,7 @@ class SQLCompiler:
     def get_combinator_sql(self, combinator, all):
         features = self.connection.features
         compilers = [
-            query.get_compiler(self.using, self.connection)
+            query.clone().get_compiler(self.using, self.connection)
             for query in self.query.combined_queries if not query.is_empty()
         ]
         if not features.supports_slicing_ordering_in_compound:

```
