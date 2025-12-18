# Failure Analysis: django__django-11400

## Basic Info
```
{
  "exit_status": "Submitted",
  "api_calls": 46,
  "cost": 0.5523216000000001
}
```

## Token Usage
- Max prompt tokens: 29736

## Files Modified in Submission
```
- django/contrib/admin/filters.py
```

## Rule Violation Check

## Agent Reasoning About Tests
```
I'll modify `reproduce_issue.py` to add a test case for explicit empty ordering in `ModelAdmin`.
The instructions say "DO NOT MODIFY: Tests".
"Your task is specifically to make changes to non-test files in the current directory in order to fix the issue described in the PR description in a way that is general and consistent with the codebase."
So I should NOT modify the tests. I've verified my fix with `reproduce_issue.py` and verified consistency with `ChangeList` behavior.
```

## Submission Diff (first 100 lines)
```diff
diff --git a/django/contrib/admin/filters.py b/django/contrib/admin/filters.py
index d65e01d5e2..5be95e2232 100644
--- a/django/contrib/admin/filters.py
+++ b/django/contrib/admin/filters.py
@@ -194,11 +194,11 @@ class RelatedFieldListFilter(FieldListFilter):
         return [self.lookup_kwarg, self.lookup_kwarg_isnull]
 
     def field_choices(self, field, request, model_admin):
-        ordering = ()
+        ordering = None
         related_admin = model_admin.admin_site._registry.get(field.remote_field.model)
         if related_admin is not None:
             ordering = related_admin.get_ordering(request)
-        return field.get_choices(include_blank=False, ordering=ordering)
+        return field.get_choices(include_blank=False, ordering=ordering or field.remote_field.model._meta.ordering)
 
     def choices(self, changelist):
         yield {
@@ -419,4 +419,8 @@ FieldListFilter.register(lambda f: True, AllValuesFieldListFilter)
 class RelatedOnlyFieldListFilter(RelatedFieldListFilter):
     def field_choices(self, field, request, model_admin):
         pk_qs = model_admin.get_queryset(request).distinct().values_list('%s__pk' % self.field_path, flat=True)
-        return field.get_choices(include_blank=False, limit_choices_to={'pk__in': pk_qs})
+        ordering = None
+        related_admin = model_admin.admin_site._registry.get(field.remote_field.model)
+        if related_admin is not None:
+            ordering = related_admin.get_ordering(request)
+        return field.get_choices(include_blank=False, limit_choices_to={'pk__in': pk_qs}, ordering=ordering or field.remote_field.model._meta.ordering)

```
