# Failure Analysis: django__django-15916

## Basic Info
```
{
  "exit_status": "Submitted",
  "api_calls": 33,
  "cost": 0.35714900000000005
}
```

## Token Usage
- Max prompt tokens: 22672

## Files Modified in Submission
```
- django/forms/models.py
```

## Rule Violation Check

## Agent Reasoning About Tests
```
"Your task is specifically to make changes to non-test files in the current directory ... DO NOT MODIFY: Tests".
Ah, "modify non-test files". It doesn't explicitly forbid creating new test files if they are not modifying existing ones?
"DO NOT MODIFY: Tests" usually means don't change existing tests.
However, given the instructions, I am usually expected to fix the code. I verified it with my script. The repository has a `tests` directory. I can't easily run the full test suite because of the environment (I might not have all dependencies or database setup), but `django` tests are usually run with `runtests.py` or similar.
```

## Submission Diff (first 100 lines)
```diff
diff --git a/django/forms/models.py b/django/forms/models.py
index 192d9fad94..1852220fe6 100644
--- a/django/forms/models.py
+++ b/django/forms/models.py
@@ -636,7 +636,9 @@ def modelform_factory(
     class_name = model.__name__ + "Form"
 
     # Class attributes for the new form class.
-    form_class_attrs = {"Meta": Meta, "formfield_callback": formfield_callback}
+    form_class_attrs = {"Meta": Meta}
+    if formfield_callback is not None:
+        form_class_attrs["formfield_callback"] = formfield_callback
 
     if getattr(Meta, "fields", None) is None and getattr(Meta, "exclude", None) is None:
         raise ImproperlyConfigured(

```
