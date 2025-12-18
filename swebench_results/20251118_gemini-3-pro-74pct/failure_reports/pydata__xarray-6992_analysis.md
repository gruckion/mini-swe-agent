# Failure Analysis: pydata__xarray-6992

## Basic Info
```
{
  "exit_status": "Submitted",
  "api_calls": 36,
  "cost": 0.28915320000000005
}
```

## Token Usage
- Max prompt tokens: 15172

## Files Modified in Submission
```
- xarray/core/dataset.py
```

## Rule Violation Check

## Agent Reasoning About Tests
```
```

## Submission Diff (first 100 lines)
```diff
diff --git a/xarray/core/dataset.py b/xarray/core/dataset.py
index 620f32f8..e6cdddb0 100644
--- a/xarray/core/dataset.py
+++ b/xarray/core/dataset.py
@@ -365,7 +365,7 @@ class DataVariables(Mapping[Any, "DataArray"]):
         )
 
     def __len__(self) -> int:
-        return len(self._dataset._variables) - len(self._dataset._coord_names)
+        return len(self._dataset._variables) - len(self._dataset._variables.keys() & self._dataset._coord_names)
 
     def __contains__(self, key: Hashable) -> bool:
         return key in self._dataset._variables and key not in self._dataset._coord_names

```
