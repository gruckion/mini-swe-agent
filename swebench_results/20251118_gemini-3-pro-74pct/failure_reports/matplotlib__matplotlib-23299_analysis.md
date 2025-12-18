# Failure Analysis: matplotlib__matplotlib-23299

## Basic Info
```
{
  "exit_status": "Submitted",
  "api_calls": 70,
  "cost": 0.6759616
}
```

## Token Usage
- Max prompt tokens: 31004

## Files Modified in Submission
```
- lib/matplotlib/pyplot.py
```

## Rule Violation Check

## Agent Reasoning About Tests
```
```

## Submission Diff (first 100 lines)
```diff
diff --git a/lib/matplotlib/pyplot.py b/lib/matplotlib/pyplot.py
index e3c66ea67c..ff404035e9 100644
--- a/lib/matplotlib/pyplot.py
+++ b/lib/matplotlib/pyplot.py
@@ -222,7 +222,6 @@ def switch_backend(newbackend):
     global _backend_mod
     # make sure the init is pulled up so we can assign to it later
     import matplotlib.backends
-    close("all")
 
     if newbackend is rcsetup._auto_backend_sentinel:
         current_framework = cbook._get_running_interactive_framework()
@@ -260,8 +259,15 @@ def switch_backend(newbackend):
             rcParamsOrig["backend"] = "agg"
             return
 
-    backend_mod = importlib.import_module(
-        cbook._backend_module_name(newbackend))
+    module_name = cbook._backend_module_name(newbackend)
+    if _backend_mod is not None:
+        canvas_class = getattr(_backend_mod, "FigureCanvas", None)
+        if canvas_class is not None and canvas_class.__module__ == module_name:
+            rcParams["backend"] = rcParamsDefault["backend"] = newbackend
+            return
+    close("all")
+
+    backend_mod = importlib.import_module(module_name)
     canvas_class = backend_mod.FigureCanvas
 
     required_framework = _get_required_interactive_framework(backend_mod)

```
