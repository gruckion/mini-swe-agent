# Failure Analysis: matplotlib__matplotlib-23476

## Basic Info
```
{
  "exit_status": "Submitted",
  "api_calls": 24,
  "cost": 0.41123380000000004
}
```

## Token Usage
- Max prompt tokens: 29331

## Files Modified in Submission
```
- lib/matplotlib/backends/backend_macosx.py
- sinus.pickle
```

## Rule Violation Check

## Agent Reasoning About Tests
```
```

## Submission Diff (first 100 lines)
```diff
diff --git a/lib/matplotlib/backends/backend_macosx.py b/lib/matplotlib/backends/backend_macosx.py
index 700d1d4c58..481bf0a626 100644
--- a/lib/matplotlib/backends/backend_macosx.py
+++ b/lib/matplotlib/backends/backend_macosx.py
@@ -36,7 +36,10 @@ class FigureCanvasMac(FigureCanvasAgg, _macosx.FigureCanvas, FigureCanvasBase):
     manager_class = _api.classproperty(lambda cls: FigureManagerMac)
 
     def __init__(self, figure):
+        _dpi = figure.dpi
         super().__init__(figure=figure)
+        if figure.dpi != _dpi:
+            figure.dpi = _dpi
         self._draw_pending = False
         self._is_drawing = False
 
diff --git a/sinus.pickle b/sinus.pickle
new file mode 100644
index 0000000000..fa9722ee92
Binary files /dev/null and b/sinus.pickle differ

```
