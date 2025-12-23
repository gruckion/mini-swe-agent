# Failure Analysis: scikit-learn__scikit-learn-26194

## Basic Info
```
{
  "exit_status": "Submitted",
  "api_calls": 18,
  "cost": 0.2428176
}
```

## Token Usage
- Max prompt tokens: 17575

## Files Modified in Submission
```
- sklearn/metrics/_ranking.py
```

## Rule Violation Check

## Agent Reasoning About Tests
```
THOUGHT: I have fixed the issue where `roc_curve` thresholds could exceed 1 when providing probability estimates (specifically when max score < 1). I verified the fix with a reproduction script and edge cases, and ensured no regression with existing tests.
```

## Submission Diff (first 100 lines)
```diff
diff --git a/sklearn/metrics/_ranking.py b/sklearn/metrics/_ranking.py
index 0cdead923..b51a5c9e8 100644
--- a/sklearn/metrics/_ranking.py
+++ b/sklearn/metrics/_ranking.py
@@ -1083,7 +1083,10 @@ def roc_curve(
     # to make sure that the curve starts at (0, 0)
     tps = np.r_[0, tps]
     fps = np.r_[0, fps]
-    thresholds = np.r_[thresholds[0] + 1, thresholds]
+    if thresholds.size > 0 and thresholds[0] < 1:
+        thresholds = np.r_[1, thresholds]
+    else:
+        thresholds = np.r_[thresholds[0] + 1, thresholds]
 
     if fps[-1] <= 0:
         warnings.warn(

```
