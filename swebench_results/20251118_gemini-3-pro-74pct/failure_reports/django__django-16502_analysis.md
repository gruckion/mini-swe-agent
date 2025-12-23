# Failure Analysis: django__django-16502

## Basic Info
```
{
  "exit_status": "Submitted",
  "api_calls": 28,
  "cost": 0.4138424
}
```

## Token Usage
- Max prompt tokens: 30077

## Files Modified in Submission
```
- django/core/servers/basehttp.py
```

## Rule Violation Check

## Agent Reasoning About Tests
```
        This fix applies only for testserver/runserver.
I'll modify `reproduction/test_issue.sh` to grep for `Content-Length`.
```

## Submission Diff (first 100 lines)
```diff
diff --git a/django/core/servers/basehttp.py b/django/core/servers/basehttp.py
index fef5532e58..809290e270 100644
--- a/django/core/servers/basehttp.py
+++ b/django/core/servers/basehttp.py
@@ -128,6 +128,20 @@ class ServerHandler(simple_server.ServerHandler):
             LimitedStream(stdin, content_length), stdout, stderr, environ, **kwargs
         )
 
+    def finish_response(self):
+        if self.environ["REQUEST_METHOD"] == "HEAD":
+            try:
+                for _ in self.result:
+                    pass
+            finally:
+                try:
+                    if not self.headers_sent:
+                        self.send_headers()
+                finally:
+                    self.close()
+        else:
+            super().finish_response()
+
     def cleanup_headers(self):
         super().cleanup_headers()
         # HTTP/1.1 requires support for persistent connections. Send 'close' if

```
