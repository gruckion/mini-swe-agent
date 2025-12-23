# Failure Analysis: sphinx-doc__sphinx-10435

## Basic Info
```
{
  "exit_status": "Submitted",
  "api_calls": 35,
  "cost": 0.3121408
}
```

## Token Usage
- Max prompt tokens: 22921

## Files Modified in Submission
```
- sphinx/writers/latex.py
- tox.ini
```

## Rule Violation Check

## Agent Reasoning About Tests
```
cat reproduction/_build/latex_fixed/testproject.tex
```

## Submission Diff (first 100 lines)
```diff
diff --git a/sphinx/writers/latex.py b/sphinx/writers/latex.py
index e0c7d56f8..448054352 100644
--- a/sphinx/writers/latex.py
+++ b/sphinx/writers/latex.py
@@ -1710,9 +1710,11 @@ class LaTeXTranslator(SphinxTranslator):
         # TODO: Use nowrap option once LaTeX formatter supports it
         # https://github.com/pygments/pygments/pull/1343
         hlcode = hlcode.replace(r'\begin{Verbatim}[commandchars=\\\{\}]',
-                                r'\sphinxcode{\sphinxupquote{')
+                                r'\sphinxcode{\sphinxupquote{%')
         # get consistent trailer
         hlcode = hlcode.rstrip()[:-14]  # strip \end{Verbatim}
+        if hlcode.endswith('\n'):
+            hlcode = hlcode[:-1]
         self.body.append(hlcode)
         self.body.append('}}')
         raise nodes.SkipNode
@@ -1784,6 +1786,8 @@ class LaTeXTranslator(SphinxTranslator):
                                         r'\begin{sphinxVerbatim}')
             # get consistent trailer
             hlcode = hlcode.rstrip()[:-14]  # strip \end{Verbatim}
+        if hlcode.endswith('\n'):
+            hlcode = hlcode[:-1]
             if self.table and not self.in_footnote:
                 hlcode += r'\end{sphinxVerbatimintable}'
             else:
diff --git a/tox.ini b/tox.ini
index 105a02597..90ada0821 100644
--- a/tox.ini
+++ b/tox.ini
@@ -29,7 +29,7 @@ setenv =
     PYTHONWARNINGS = all
     PYTEST_ADDOPTS = {env:PYTEST_ADDOPTS:} --color yes
 commands=
-    python -X dev -X warn_default_encoding -m pytest --durations 25 {posargs}
+    python -X dev -X warn_default_encoding -m pytest -rA --durations 25 {posargs}
 
 [testenv:du-latest]
 commands =

```
