# Failure Analysis: matplotlib__matplotlib-25479

## Basic Info
```
{
  "exit_status": "Submitted",
  "api_calls": 34,
  "cost": 0.42836439999999987
}
```

## Token Usage
- Max prompt tokens: 27122

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
index 58ce4c03fa..52a6c21f2a 100644
--- a/lib/matplotlib/pyplot.py
+++ b/lib/matplotlib/pyplot.py
@@ -2278,9 +2278,18 @@ def set_cmap(cmap: Colormap | str) -> None:
     matplotlib.cm.register_cmap
     matplotlib.cm.get_cmap
     """
+    if isinstance(cmap, str):
+        cmap_name = cmap
+    elif cmap is None:
+        cmap_name = matplotlib.rcParams["image.cmap"]
+    else:
+        cmap_name = None
+
     cmap = get_cmap(cmap)
+    if cmap_name is None:
+        cmap_name = cmap.name
 
-    rc('image', cmap=cmap.name)
+    rc("image", cmap=cmap_name)
     im = gci()
 
     if im is not None:

```
