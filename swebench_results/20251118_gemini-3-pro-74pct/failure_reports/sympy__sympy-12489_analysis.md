# Failure Analysis: sympy__sympy-12489

## Basic Info
```
{
  "exit_status": "Submitted",
  "api_calls": 73,
  "cost": 0.7632313999999998
}
```

## Token Usage
- Max prompt tokens: 25828

## Files Modified in Submission
```
- sympy/combinatorics/permutations.py
```

## Rule Violation Check

## Agent Reasoning About Tests
```
But first, let's make sure I didn't break anything with my current changes. I already ran tests and they passed.
```

## Submission Diff (first 100 lines)
```diff
diff --git a/sympy/combinatorics/permutations.py b/sympy/combinatorics/permutations.py
index 4ac1c2ef3b..0f668b9067 100644
--- a/sympy/combinatorics/permutations.py
+++ b/sympy/combinatorics/permutations.py
@@ -857,19 +857,19 @@ def __new__(cls, *args, **kwargs):
         #g) (Permutation) = adjust size or return copy
         ok = True
         if not args:  # a
-            return _af_new(list(range(size or 0)))
+            return cls._af_new(list(range(size or 0)))
         elif len(args) > 1:  # c
-            return _af_new(Cycle(*args).list(size))
+            return cls._af_new(Cycle(*args).list(size))
         if len(args) == 1:
             a = args[0]
             if isinstance(a, Perm):  # g
-                if size is None or size == a.size:
+                if (size is None or size == a.size) and isinstance(a, cls):
                     return a
-                return Perm(a.array_form, size=size)
+                return cls(a.array_form, size=size)
             if isinstance(a, Cycle):  # f
-                return _af_new(a.list(size))
+                return cls._af_new(a.list(size))
             if not is_sequence(a):  # b
-                return _af_new(list(range(a + 1)))
+                return cls._af_new(list(range(a + 1)))
             if has_variety(is_sequence(ai) for ai in a):
                 ok = False
         else:
@@ -924,8 +924,8 @@ def __new__(cls, *args, **kwargs):
         obj._size = size
         return obj
 
-    @staticmethod
-    def _af_new(perm):
+    @classmethod
+    def _af_new(cls, perm):
         """A method to produce a Permutation object from a list;
         the list is bound to the _array_form attribute, so it must
         not be modified; this method is meant for internal use only;
@@ -944,7 +944,7 @@ def _af_new(perm):
         Permutation([2, 1, 3, 0])
 
         """
-        p = Basic.__new__(Perm, perm)
+        p = Basic.__new__(cls, perm)
         p._array_form = perm
         p._size = len(perm)
         return p
@@ -1499,7 +1499,7 @@ def from_sequence(self, i, key=None):
             ic.sort(key=lambda x: key(x[0]))
         else:
             ic.sort()
-        return ~Permutation([i[1] for i in ic])
+        return self._af_new(_af_invert([i[1] for i in ic]))
 
     def __invert__(self):
         """
@@ -2734,7 +2734,7 @@ def from_inversion_vector(self, inversion):
         except IndexError:
             raise ValueError("The inversion vector is not valid.")
         perm.extend(N)
-        return _af_new(perm)
+        return self._af_new(perm)
 
     @classmethod
     def random(self, n):
@@ -2753,7 +2753,7 @@ def random(self, n):
         """
         perm_array = list(range(n))
         random.shuffle(perm_array)
-        return _af_new(perm_array)
+        return self._af_new(perm_array)
 
     @classmethod
     def unrank_lex(self, size, rank):

```
