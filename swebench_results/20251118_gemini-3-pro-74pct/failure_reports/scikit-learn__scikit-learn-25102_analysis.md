# Failure Analysis: scikit-learn__scikit-learn-25102

## Basic Info
```
{
  "exit_status": "Submitted",
  "api_calls": 43,
  "cost": 1.9857164
}
```

## Token Usage
- Max prompt tokens: 106497

## Files Modified in Submission
```
- sklearn/compose/_column_transformer.py
- sklearn/pipeline.py
- sklearn/preprocessing/_function_transformer.py
- sklearn/utils/_set_output.py
```

## Rule Violation Check

## Agent Reasoning About Tests
```
Let's update the reproduction script to test the new feature.
THOUGHT: `sklearn/compose/tests/test_column_transformer.py` has a mock class with `set_output`. I should not modify tests.
```

## Submission Diff (first 100 lines)
```diff
diff --git a/sklearn/compose/_column_transformer.py b/sklearn/compose/_column_transformer.py
index 5f76c2cc9..d340331aa 100644
--- a/sklearn/compose/_column_transformer.py
+++ b/sklearn/compose/_column_transformer.py
@@ -271,7 +271,7 @@ class ColumnTransformer(TransformerMixin, _BaseComposition):
         except (TypeError, ValueError):
             self.transformers = value
 
-    def set_output(self, *, transform=None):
+    def set_output(self, *, transform=None, **kwargs):
         """Set the output container when `"transform"` and `"fit_transform"` are called.
 
         Calling `set_output` will set the output of all estimators in `transformers`
@@ -300,7 +300,7 @@ class ColumnTransformer(TransformerMixin, _BaseComposition):
             if trans not in {"passthrough", "drop"}
         )
         for trans in transformers:
-            _safe_set_output(trans, transform=transform)
+            _safe_set_output(trans, transform=transform, **kwargs)
 
         return self
 
diff --git a/sklearn/pipeline.py b/sklearn/pipeline.py
index 94d9465d7..fa55ac537 100644
--- a/sklearn/pipeline.py
+++ b/sklearn/pipeline.py
@@ -154,7 +154,7 @@ class Pipeline(_BaseComposition):
         self.memory = memory
         self.verbose = verbose
 
-    def set_output(self, *, transform=None):
+    def set_output(self, *, transform=None, **kwargs):
         """Set the output container when `"transform"` and `"fit_transform"` are called.
 
         Calling `set_output` will set the output of all estimators in `steps`.
@@ -174,7 +174,7 @@ class Pipeline(_BaseComposition):
             Estimator instance.
         """
         for _, _, step in self._iter():
-            _safe_set_output(step, transform=transform)
+            _safe_set_output(step, transform=transform, **kwargs)
         return self
 
     def get_params(self, deep=True):
@@ -1027,7 +1027,7 @@ class FeatureUnion(TransformerMixin, _BaseComposition):
         self.transformer_weights = transformer_weights
         self.verbose = verbose
 
-    def set_output(self, *, transform=None):
+    def set_output(self, *, transform=None, **kwargs):
         """Set the output container when `"transform"` and `"fit_transform"` are called.
 
         `set_output` will set the output of all estimators in `transformer_list`.
diff --git a/sklearn/preprocessing/_function_transformer.py b/sklearn/preprocessing/_function_transformer.py
index a4f5448a0..3df7c1b74 100644
--- a/sklearn/preprocessing/_function_transformer.py
+++ b/sklearn/preprocessing/_function_transformer.py
@@ -316,7 +316,7 @@ class FunctionTransformer(TransformerMixin, BaseEstimator):
     def _more_tags(self):
         return {"no_validation": not self.validate, "stateless": True}
 
-    def set_output(self, *, transform=None):
+    def set_output(self, *, transform=None, **kwargs):
         """Set output container.
 
         See :ref:`sphx_glr_auto_examples_miscellaneous_plot_set_output.py`
@@ -337,7 +337,7 @@ class FunctionTransformer(TransformerMixin, BaseEstimator):
             Estimator instance.
         """
         if hasattr(super(), "set_output"):
-            return super().set_output(transform=transform)
+            return super().set_output(transform=transform, **kwargs)
 
         if transform == "pandas" and self.feature_names_out is None:
             warnings.warn(
diff --git a/sklearn/utils/_set_output.py b/sklearn/utils/_set_output.py
index 335773c6a..6c75c9f46 100644
--- a/sklearn/utils/_set_output.py
+++ b/sklearn/utils/_set_output.py
@@ -12,6 +12,7 @@ def _wrap_in_pandas_container(
     *,
     columns,
     index=None,
+    dtypes=None,
 ):
     """Create a Pandas DataFrame.
 
@@ -36,6 +37,10 @@ def _wrap_in_pandas_container(
     index : array-like, default=None
         Index for data.
 
+    dtypes : dict, default=None
+        Dictionary with keys as column names and values as dtypes.
+        If not None, the dtypes of the output DataFrame will be set to these values.
+
     Returns
     -------
     dataframe : DataFrame
@@ -57,9 +62,20 @@ def _wrap_in_pandas_container(
             data_to_wrap.columns = columns
```
