# Failure Analysis: psf__requests-6028

## Basic Info
```
{
  "exit_status": "Submitted",
  "api_calls": 49,
  "cost": 0.5777244000000001
}
```

## Token Usage
- Max prompt tokens: 36654

## Files Modified in Submission
```
- requests/utils.py
```

## Rule Violation Check

## Agent Reasoning About Tests
```
THOUGHT: The errors are due to `fixture 'mocker' not found`. This means `pytest-mock` is not installed. I should install it to run the tests properly.
THOUGHT: All tests passed. This confirms that my change didn't break existing functionality covered by tests.
THOUGHT: The errors in `tests/test_requests.py` seem related to `httpbin` fixture recursive dependency. This might be an issue with the test environment or `pytest-httpbin` plugin.
To be sure, I should revert my changes and run the tests again to confirm these failures are pre-existing.
```

## Submission Diff (first 100 lines)
```diff
diff --git a/requests/utils.py b/requests/utils.py
index 1c2ae4e0..49128207 100644
--- a/requests/utils.py
+++ b/requests/utils.py
@@ -988,12 +988,22 @@ def get_auth_from_url(url):
 
     :rtype: (str,str)
     """
-    parsed = urlparse(url)
+    parsed = parse_url(url)
 
     try:
-        auth = (unquote(parsed.username), unquote(parsed.password))
-    except (AttributeError, TypeError):
-        auth = ('', '')
+        auth = parsed.auth
+    except AttributeError:
+        auth = None
+
+    if not auth:
+        return ('', '')
+
+    parts = auth.split(':', 1)
+
+    if len(parts) == 2:
+        return (unquote(parts[0]), unquote(parts[1]))
+
+    return ('', '')
 
     return auth
 

```
