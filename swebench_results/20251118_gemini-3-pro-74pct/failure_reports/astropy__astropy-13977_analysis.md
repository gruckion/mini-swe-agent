# Failure Analysis: astropy__astropy-13977

## Basic Info
```
{
  "exit_status": "Submitted",
  "api_calls": 28,
  "cost": 0.28858120000000004
}
```

## Token Usage
- Max prompt tokens: 20360

## Files Modified in Submission
```
- astropy/units/quantity.py
- astropy/units/tests/test_quantity_duck_typing.py
- pyproject.toml
```

## Rule Violation Check
### ❌ TEST FILES MODIFIED
```
diff --git a/astropy/units/tests/test_quantity_duck_typing.py b/astropy/units/tests/test_quantity_duck_typing.py
+++ b/astropy/units/tests/test_quantity_duck_typing.py
```
### ❌ CONFIG FILES MODIFIED
```
diff --git a/pyproject.toml b/pyproject.toml
--- a/pyproject.toml
+++ b/pyproject.toml
```

## Agent Reasoning About Tests
```
I should update the test to use `u.isclose` or compare with tolerance.
```

## Submission Diff (first 100 lines)
```diff
diff --git a/astropy/units/quantity.py b/astropy/units/quantity.py
index b98abfafb0..35de91cba3 100644
--- a/astropy/units/quantity.py
+++ b/astropy/units/quantity.py
@@ -667,7 +667,13 @@ class Quantity(np.ndarray):
         arrays = []
         for input_, converter in zip(inputs, converters):
             input_ = getattr(input_, "value", input_)
-            arrays.append(converter(input_) if converter else input_)
+            if converter:
+                try:
+                    arrays.append(converter(input_))
+                except ValueError:
+                    return NotImplemented
+            else:
+                arrays.append(input_)
 
         # Call our superclass's __array_ufunc__
         result = super().__array_ufunc__(function, method, *arrays, **kwargs)
diff --git a/astropy/units/tests/test_quantity_duck_typing.py b/astropy/units/tests/test_quantity_duck_typing.py
new file mode 100644
index 0000000000..939949a20a
--- /dev/null
+++ b/astropy/units/tests/test_quantity_duck_typing.py
@@ -0,0 +1,54 @@
+import dataclasses
+import pytest
+import numpy as np
+import astropy.units as u
+
+@dataclasses.dataclass
+class DuckArray(np.lib.mixins.NDArrayOperatorsMixin):
+    ndarray: u.Quantity
+
+    @property
+    def unit(self) -> u.UnitBase:
+        return self.ndarray.unit
+
+    def __array_ufunc__(self, function, method, *inputs, **kwargs):
+        inputs = [inp.ndarray if isinstance(inp, DuckArray) else inp for inp in inputs]
+
+        for inp in inputs:
+            if isinstance(inp, np.ndarray):
+                result = inp.__array_ufunc__(function, method, *inputs, **kwargs)
+                if result is not NotImplemented:
+                    return DuckArray(result)
+
+        return NotImplemented
+
+def test_duck_array_radd():
+    # This was the issue reported in the PR
+    # (1 * u.m) + DuckArray(1 * u.mm) should work via DuckArray.__radd__
+    # which is called because Quantity.__add__ returns NotImplemented
+    
+    d = DuckArray(1 * u.mm)
+    q = 1 * u.m
+    
+    # Case 1: DuckArray on left (worked before)
+    res1 = d + q
+    assert isinstance(res1, DuckArray)
+    # Use isclose for floating point comparison
+    assert u.isclose(res1.ndarray, 1.001 * u.m)
+    
+    # Case 2: DuckArray on right (failed before)
+    res2 = q + d
+    assert isinstance(res2, DuckArray)
+    assert u.isclose(res2.ndarray, 1.001 * u.m)
+
+def test_invalid_type_raises_typeerror():
+    # Ensure that invalid types now raise TypeError instead of ValueError
+    # because Quantity returns NotImplemented and Python raises TypeError
+    
+    q = 1 * u.m
+    
+    with pytest.raises(TypeError, match="Unsupported operand type"):
+        q + "string"
+        
+    with pytest.raises(TypeError, match="Unsupported operand type"):
+        q + object()
diff --git a/pyproject.toml b/pyproject.toml
index 486d6b9b3b..1c5f74f3a1 100644
--- a/pyproject.toml
+++ b/pyproject.toml
@@ -1,5 +1,5 @@
 [build-system]
-requires = ["setuptools",
+requires = ["setuptools==68.0.0",
             "setuptools_scm>=6.2",
             "wheel",
             "cython==0.29.30",

```
