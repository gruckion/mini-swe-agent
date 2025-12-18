# Failure Analysis: django__django-12406

## Basic Info
```
{
  "exit_status": "Submitted",
  "api_calls": 54,
  "cost": 0.6799664000000001
}
```

## Token Usage
- Max prompt tokens: 31388

## Files Modified in Submission
```
- django/forms/models.py
```

## Rule Violation Check

## Agent Reasoning About Tests
```
```

## Submission Diff (first 100 lines)
```diff
diff --git a/django/forms/models.py b/django/forms/models.py
index dafc11f995..ce97871e9c 100644
--- a/django/forms/models.py
+++ b/django/forms/models.py
@@ -13,7 +13,7 @@ from django.forms.forms import BaseForm, DeclarativeFieldsMetaclass
 from django.forms.formsets import BaseFormSet, formset_factory
 from django.forms.utils import ErrorList
 from django.forms.widgets import (
-    HiddenInput, MultipleHiddenInput, SelectMultiple,
+    HiddenInput, MultipleHiddenInput, SelectMultiple, RadioSelect,
 )
 from django.utils.text import capfirst, get_text_list
 from django.utils.translation import gettext, gettext_lazy as _
@@ -1188,7 +1188,10 @@ class ModelChoiceField(ChoiceField):
         if required and (initial is not None):
             self.empty_label = None
         else:
-            self.empty_label = empty_label
+            if required and isinstance(widget, RadioSelect) or (isinstance(widget, type) and issubclass(widget, RadioSelect)):
+                self.empty_label = empty_label if empty_label != '---------' else None
+            else:
+                self.empty_label = empty_label
 
         # Call Field instead of ChoiceField __init__() because we don't need
         # ChoiceField.__init__().

```
