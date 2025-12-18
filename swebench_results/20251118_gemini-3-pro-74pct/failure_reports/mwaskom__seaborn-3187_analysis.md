# Failure Analysis: mwaskom__seaborn-3187

## Basic Info
```
{
  "exit_status": "Submitted",
  "api_calls": 42,
  "cost": 0.5055436
}
```

## Token Usage
- Max prompt tokens: 24364

## Files Modified in Submission
```
- seaborn/_core/plot.py
- seaborn/_core/scales.py
```

## Rule Violation Check

## Agent Reasoning About Tests
```
The instruction says: "Your task is specifically to make changes to non-test files in the current directory in order to fix the issue described in the PR description in a way that is general and consistent with the codebase."
```

## Submission Diff (first 100 lines)
```diff
diff --git a/seaborn/_core/plot.py b/seaborn/_core/plot.py
index 8915616b..95fb1581 100644
--- a/seaborn/_core/plot.py
+++ b/seaborn/_core/plot.py
@@ -1561,7 +1561,7 @@ class Plotter:
         for var in legend_vars:
             var_legend = scales[var]._legend
             if var_legend is not None:
-                values, labels = var_legend
+                values, labels, *suffix = var_legend
                 for (_, part_id), part_vars, _ in schema:
                     if data.ids[var] == part_id:
                         # Allow multiple plot semantics to represent same data variable
@@ -1569,6 +1569,8 @@ class Plotter:
                         break
                 else:
                     title = self._resolve_label(p, var, data.names[var])
+                    if suffix:
+                        title = f"{title} ({suffix[0]})"
                     entry = (title, data.ids[var]), [var], (values, labels)
                     schema.append(entry)
 
diff --git a/seaborn/_core/scales.py b/seaborn/_core/scales.py
index 55874bf2..f23903bb 100644
--- a/seaborn/_core/scales.py
+++ b/seaborn/_core/scales.py
@@ -60,7 +60,7 @@ class Scale:
     _pipeline: Pipeline
     _matplotlib_scale: ScaleBase
     _spacer: staticmethod
-    _legend: tuple[list[str], list[Any]] | None
+    _legend: Any | None
 
     def __post_init__(self):
 
@@ -380,6 +380,11 @@ class ContinuousBase(Scale):
             locs = locs[(vmin <= locs) & (locs <= vmax)]
             labels = axis.major.formatter.format_ticks(locs)
             new._legend = list(locs), list(labels)
+            formatter = axis.major.formatter
+            if hasattr(formatter, "get_offset"):
+                offset = formatter.get_offset()
+                if offset:
+                    new._legend += (offset,)
 
         return new
 

```
