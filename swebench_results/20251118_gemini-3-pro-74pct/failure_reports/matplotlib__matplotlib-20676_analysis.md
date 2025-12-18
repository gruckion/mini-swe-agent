# Failure Analysis: matplotlib__matplotlib-20676

## Basic Info
```
{
  "exit_status": "Submitted",
  "api_calls": 51,
  "cost": 0.561696
}
```

## Token Usage
- Max prompt tokens: 25628

## Files Modified in Submission
```
- lib/matplotlib/widgets.py
```

## Rule Violation Check

## Agent Reasoning About Tests
```
I should update `test_selection.py` to use the public methods `press`, `onmove`, `release`.
THOUGHT: Now I verify the fix again with `reproduce_issue.py` and `test_selection.py`.
```

## Submission Diff (first 100 lines)
```diff
diff --git a/lib/matplotlib/widgets.py b/lib/matplotlib/widgets.py
index a199e45d40..03ee472b33 100644
--- a/lib/matplotlib/widgets.py
+++ b/lib/matplotlib/widgets.py
@@ -2141,10 +2141,12 @@ class SpanSelector(_SelectorWidget):
         if self.direction == 'horizontal':
             trans = ax.get_xaxis_transform()
             w, h = 0, 1
+            rect_xy = (np.nan, 0)
         else:
             trans = ax.get_yaxis_transform()
             w, h = 1, 0
-        self._rect = Rectangle((0, 0), w, h,
+            rect_xy = (0, np.nan)
+        self._rect = Rectangle(rect_xy, w, h,
                                transform=trans,
                                visible=False,
                                **self._rectprops)

```
