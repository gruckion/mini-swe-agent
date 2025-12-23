# Failure Analysis: django__django-14011

## Basic Info
```
{
  "exit_status": "Submitted",
  "api_calls": 29,
  "cost": 0.4360774
}
```

## Token Usage
- Max prompt tokens: 27196

## Files Modified in Submission
```
- django/core/servers/basehttp.py
```

## Rule Violation Check

## Agent Reasoning About Tests
```
"Issue #20238 added threading support to LiveServerTestCase. One of the changes it made ​was changing LiveServerThread to use ThreadedWSGIServer instead of WSGIServer. LiveServerThread is used by LiveServerTestCase."
Wait, `LiveServerTestCase` creates a test database. The settings I provided use `test_db.sqlite3` as the NAME. `LiveServerTestCase` (via `TransactionTestCase` -> `TestCase`) will create a test database, usually prefixed with `test_`.
THOUGHT: I should double check if I need to keep the test. The instructions say "MODIFY: Regular source code files in /testbed". "DO NOT MODIFY: Tests".
However, adding a new test file is usually good practice, but the instructions say "DO NOT MODIFY: Tests". It might mean existing tests. But usually I should not leave new files unless they are part of the PR.
The instructions say: "Your task is specifically to make changes to non-test files in the current directory in order to fix the issue described in the PR description".
```

## Submission Diff (first 100 lines)
```diff
diff --git a/django/core/servers/basehttp.py b/django/core/servers/basehttp.py
index 14dab517c9..0429ed8b8a 100644
--- a/django/core/servers/basehttp.py
+++ b/django/core/servers/basehttp.py
@@ -81,6 +81,13 @@ class ThreadedWSGIServer(socketserver.ThreadingMixIn, WSGIServer):
     """A threaded version of the WSGIServer"""
     daemon_threads = True
 
+    def process_request_thread(self, request, client_address):
+        try:
+            super().process_request_thread(request, client_address)
+        finally:
+            from django.db import connections
+            connections.close_all()
+
 
 class ServerHandler(simple_server.ServerHandler):
     http_version = '1.1'

```
