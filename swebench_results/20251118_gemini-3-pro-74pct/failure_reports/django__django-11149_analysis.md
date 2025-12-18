# Failure Analysis: django__django-11149

## Basic Info
```
{
  "exit_status": "Submitted",
  "api_calls": 36,
  "cost": 0.5521938000000001
}
```

## Token Usage
- Max prompt tokens: 30290

## Files Modified in Submission
```
- django/contrib/admin/options.py
```

## Rule Violation Check

## Agent Reasoning About Tests
```
user = User.objects.create_user('editor_user', 'test@example.com', 'password')
rm reproduce_issue.py test_fix_with_permissions.py test_fix_add_view.py update_admin_options.py
```

## Submission Diff (first 100 lines)
```diff
diff --git a/django/contrib/admin/options.py b/django/contrib/admin/options.py
index 880a2cc17b..445126d0c5 100644
--- a/django/contrib/admin/options.py
+++ b/django/contrib/admin/options.py
@@ -2117,7 +2117,13 @@ class InlineModelAdmin(BaseModelAdmin):
             # which doesn't have its own individual permissions. The user needs
             # to have the view permission for the related model in order to
             # be able to do anything with the intermediate model.
-            return self.has_view_permission(request, obj)
+            if not self.has_view_permission(request, obj):
+                return False
+            if obj:
+                opts = self.parent_model._meta
+                codename = get_permission_codename('change', opts)
+                return request.user.has_perm('%s.%s' % (opts.app_label, codename))
+            return True
         return super().has_add_permission(request)
 
     def has_change_permission(self, request, obj=None):
@@ -2126,7 +2132,13 @@ class InlineModelAdmin(BaseModelAdmin):
             # which doesn't have its own individual permissions. The user needs
             # to have the view permission for the related model in order to
             # be able to do anything with the intermediate model.
-            return self.has_view_permission(request, obj)
+            if not self.has_view_permission(request, obj):
+                return False
+            if obj:
+                opts = self.parent_model._meta
+                codename = get_permission_codename('change', opts)
+                return request.user.has_perm('%s.%s' % (opts.app_label, codename))
+            return True
         return super().has_change_permission(request)
 
     def has_delete_permission(self, request, obj=None):
@@ -2135,7 +2147,13 @@ class InlineModelAdmin(BaseModelAdmin):
             # which doesn't have its own individual permissions. The user needs
             # to have the view permission for the related model in order to
             # be able to do anything with the intermediate model.
-            return self.has_view_permission(request, obj)
+            if not self.has_view_permission(request, obj):
+                return False
+            if obj:
+                opts = self.parent_model._meta
+                codename = get_permission_codename('change', opts)
+                return request.user.has_perm('%s.%s' % (opts.app_label, codename))
+            return True
         return super().has_delete_permission(request, obj)
 
     def has_view_permission(self, request, obj=None):

```
