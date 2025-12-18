# Failure Analysis: django__django-16560

## Basic Info
```
{
  "exit_status": "Submitted",
  "api_calls": 145,
  "cost": 1.4363002000000002
}
```

## Token Usage
- Max prompt tokens: 42358

## Files Modified in Submission
```
- django/db/models/constraints.py
```

## Rule Violation Check

## Agent Reasoning About Tests
```
I'll update `test_unique_constraint.py`.
sed -i "s/django.core.management.call_command('migrate', verbosity=0, interactive=False)/from django.db import connection\nwith connection.schema_editor() as schema_editor:\n    schema_editor.create_model(Product)/" test_unique_constraint.py
Wait, I cannot modify tests, but I can run them.
```

## Submission Diff (first 100 lines)
```diff
diff --git a/django/db/models/constraints.py b/django/db/models/constraints.py
index 075ecee1be..1bd95e5500 100644
--- a/django/db/models/constraints.py
+++ b/django/db/models/constraints.py
@@ -19,16 +19,18 @@ __all__ = ["BaseConstraint", "CheckConstraint", "Deferrable", "UniqueConstraint"
 class BaseConstraint:
     default_violation_error_message = _("Constraint “%(name)s” is violated.")
     violation_error_message = None
+    violation_error_code = None
 
     # RemovedInDjango60Warning: When the deprecation ends, replace with:
     # def __init__(self, *, name, violation_error_message=None):
-    def __init__(self, *args, name=None, violation_error_message=None):
+    def __init__(self, *args, name=None, violation_error_message=None, violation_error_code=None):
         # RemovedInDjango60Warning.
         if name is None and not args:
             raise TypeError(
                 f"{self.__class__.__name__}.__init__() missing 1 required keyword-only "
                 f"argument: 'name'"
             )
+        self.violation_error_code = violation_error_code
         self.name = name
         if violation_error_message is not None:
             self.violation_error_message = violation_error_message
@@ -74,21 +76,22 @@ class BaseConstraint:
             and self.violation_error_message != self.default_violation_error_message
         ):
             kwargs["violation_error_message"] = self.violation_error_message
+        if self.violation_error_code is not None:
+            kwargs["violation_error_code"] = self.violation_error_code
         return (path, (), kwargs)
 
     def clone(self):
         _, args, kwargs = self.deconstruct()
         return self.__class__(*args, **kwargs)
 
-
 class CheckConstraint(BaseConstraint):
-    def __init__(self, *, check, name, violation_error_message=None):
+    def __init__(self, *, check, name, violation_error_message=None, violation_error_code=None):
         self.check = check
         if not getattr(check, "conditional", False):
             raise TypeError(
                 "CheckConstraint.check must be a Q instance or boolean expression."
             )
-        super().__init__(name=name, violation_error_message=violation_error_message)
+        super().__init__(name=name, violation_error_message=violation_error_message, violation_error_code=violation_error_code)
 
     def _get_check_sql(self, model, schema_editor):
         query = Query(model=model, alias_cols=False)
@@ -112,12 +115,12 @@ class CheckConstraint(BaseConstraint):
         against = instance._get_field_value_map(meta=model._meta, exclude=exclude)
         try:
             if not Q(self.check).check(against, using=using):
-                raise ValidationError(self.get_violation_error_message())
+                raise ValidationError(self.get_violation_error_message(), code=self.violation_error_code)
         except FieldError:
             pass
 
     def __repr__(self):
-        return "<%s: check=%s name=%s%s>" % (
+        return "<%s: check=%s name=%s%s%s>" % (
             self.__class__.__qualname__,
             self.check,
             repr(self.name),
@@ -127,6 +130,7 @@ class CheckConstraint(BaseConstraint):
                 or self.violation_error_message == self.default_violation_error_message
                 else " violation_error_message=%r" % self.violation_error_message
             ),
+            ("" if self.violation_error_code is None else " violation_error_code=%r" % self.violation_error_code),
         )
 
     def __eq__(self, other):
@@ -135,6 +139,7 @@ class CheckConstraint(BaseConstraint):
                 self.name == other.name
                 and self.check == other.check
                 and self.violation_error_message == other.violation_error_message
+                and self.violation_error_code == other.violation_error_code
             )
         return super().__eq__(other)
 
@@ -163,7 +168,7 @@ class UniqueConstraint(BaseConstraint):
         deferrable=None,
         include=None,
         opclasses=(),
-        violation_error_message=None,
+        violation_error_message=None, violation_error_code=None,
     ):
         if not name:
             raise ValueError("A unique constraint must be named.")
@@ -213,7 +218,7 @@ class UniqueConstraint(BaseConstraint):
             F(expression) if isinstance(expression, str) else expression
             for expression in expressions
         )
-        super().__init__(name=name, violation_error_message=violation_error_message)
+        super().__init__(name=name, violation_error_message=violation_error_message, violation_error_code=violation_error_code)
 
     @property
     def contains_expressions(self):
@@ -293,7 +298,7 @@ class UniqueConstraint(BaseConstraint):
```
