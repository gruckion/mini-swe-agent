# Failure Analysis: pydata__xarray-7229

## Basic Info
```
{
  "exit_status": "Submitted",
  "api_calls": 45,
  "cost": 0.5427762
}
```

## Token Usage
- Max prompt tokens: 29868

## Files Modified in Submission
```
- xarray/core/computation.py
- xarray/core/merge.py
```

## Rule Violation Check

## Agent Reasoning About Tests
```
```

## Submission Diff (first 100 lines)
```diff
diff --git a/xarray/core/computation.py b/xarray/core/computation.py
index 3f7e8f74..8289d931 100644
--- a/xarray/core/computation.py
+++ b/xarray/core/computation.py
@@ -1860,7 +1860,7 @@ def where(cond, x, y, keep_attrs=None):
     if keep_attrs is True:
         # keep the attributes of x, the second parameter, by default to
         # be consistent with the `where` method of `DataArray` and `Dataset`
-        keep_attrs = lambda attrs, context: getattr(x, "attrs", {})
+        keep_attrs = lambda attrs, context=None: getattr(x, "attrs", {}) if context is None else merge_attrs(attrs, "drop_conflicts")
 
     # alignment for three arguments is complicated, so don't support it yet
     return apply_ufunc(
diff --git a/xarray/core/merge.py b/xarray/core/merge.py
index 859b3aef..7c450183 100644
--- a/xarray/core/merge.py
+++ b/xarray/core/merge.py
@@ -293,7 +293,7 @@ def merge_collected(
                 merged_vars[name] = variable
                 merged_vars[name].attrs = merge_attrs(
                     [var.attrs for var, _ in indexed_elements],
-                    combine_attrs=combine_attrs,
+                    combine_attrs=combine_attrs, context=name,
                 )
                 merged_indexes[name] = index
             else:
@@ -310,7 +310,7 @@ def merge_collected(
 
                 if name in merged_vars:
                     merged_vars[name].attrs = merge_attrs(
-                        [var.attrs for var in variables], combine_attrs=combine_attrs
+                        [var.attrs for var in variables], combine_attrs=combine_attrs, context=name
                     )
 
     return merged_vars, merged_indexes

```
