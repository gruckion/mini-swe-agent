# Failure Analysis: astropy__astropy-8707

## Basic Info
```
{
  "exit_status": "Submitted",
  "api_calls": 57,
  "cost": 0.4601148
}
```

## Token Usage
- Max prompt tokens: 31790

## Files Modified in Submission
```
- astropy/io/fits/card.py
- astropy/io/fits/header.py
```

## Rule Violation Check

## Agent Reasoning About Tests
```
This is unrelated to my changes. The tests are failing because of deprecation warnings being treated as errors.
I'll try to fix the test file `astropy/io/fits/tests/test_header.py` to use `setup_method` instead of `setup`. This is out of scope of the task (modifying tests), but I need to verify my changes.
"DO NOT MODIFY: Tests, configuration files (pyproject.toml, setup.cfg, etc.)"
So I cannot modify the tests.
Since I cannot modify the tests, and the failure is due to test infrastructure deprecation, I will rely on my reproduction scripts which confirmed the fix works for the reported issue and doesn't break string handling.
```

## Submission Diff (first 100 lines)
```diff
diff --git a/astropy/io/fits/card.py b/astropy/io/fits/card.py
index 8c1ac5d738..31f89e1c76 100644
--- a/astropy/io/fits/card.py
+++ b/astropy/io/fits/card.py
@@ -5,7 +5,7 @@ import warnings
 
 import numpy as np
 
-from .util import _str_to_num, _is_int, translate, _words_group
+from .util import decode_ascii, _str_to_num, _is_int, translate, _words_group
 from .verify import _Verify, _ErrList, VerifyError, VerifyWarning
 
 from . import conf
@@ -554,6 +554,9 @@ class Card(_Verify):
         """
 
         card = cls()
+        if isinstance(image, bytes):
+            image = decode_ascii(image)
+
         card._image = _pad(image)
         card._verified = False
         return card
diff --git a/astropy/io/fits/header.py b/astropy/io/fits/header.py
index ad07e6d52d..7064a7e3fa 100644
--- a/astropy/io/fits/header.py
+++ b/astropy/io/fits/header.py
@@ -348,6 +348,9 @@ class Header:
             A new `Header` instance.
         """
 
+        if isinstance(data, bytes):
+            data = decode_ascii(data)
+
         cards = []
 
         # If the card separator contains characters that may validly appear in

```
