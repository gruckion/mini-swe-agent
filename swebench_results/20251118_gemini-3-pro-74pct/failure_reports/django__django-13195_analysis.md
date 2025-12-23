# Failure Analysis: django__django-13195

## Basic Info
```
{
  "exit_status": "Submitted",
  "api_calls": 27,
  "cost": 0.3780686
}
```

## Token Usage
- Max prompt tokens: 23078

## Files Modified in Submission
```
- django/contrib/messages/storage/cookie.py
- django/contrib/sessions/middleware.py
- django/http/response.py
```

## Rule Violation Check

## Agent Reasoning About Tests
```
However, the task instructions say: "Your task is specifically to make changes to non-test files in the current directory in order to fix the issue described in the PR description in a way that is general and consistent with the codebase."
The instructions say "MODIFY: Regular source code files in /testbed".
I need to update the reproduction script to test the new arguments.
THOUGHT: I see `tests/responses/test_cookie.py`. I should not modify tests, but I should check if my changes break them.
And `docs/ref/request-response.txt` which I should probably not modify as per instructions "MODIFY: Regular source code files". Usually documentation is not required unless specified, but "Regular source code files" usually excludes docs. But if I change the signature, docs are outdated. However, the instructions say "MODIFY: Regular source code files in /testbed". Docs are usually text files. I'll skip docs.
```

## Submission Diff (first 100 lines)
```diff
diff --git a/django/contrib/messages/storage/cookie.py b/django/contrib/messages/storage/cookie.py
index 78256ca3b2..688e48b80a 100644
--- a/django/contrib/messages/storage/cookie.py
+++ b/django/contrib/messages/storage/cookie.py
@@ -92,7 +92,7 @@ class CookieStorage(BaseStorage):
                 samesite=settings.SESSION_COOKIE_SAMESITE,
             )
         else:
-            response.delete_cookie(self.cookie_name, domain=settings.SESSION_COOKIE_DOMAIN)
+            response.delete_cookie(self.cookie_name, domain=settings.SESSION_COOKIE_DOMAIN, samesite=settings.SESSION_COOKIE_SAMESITE, secure=settings.SESSION_COOKIE_SECURE or None)
 
     def _store(self, messages, response, remove_oldest=True, *args, **kwargs):
         """
diff --git a/django/contrib/sessions/middleware.py b/django/contrib/sessions/middleware.py
index 63013eef7a..ba2f9b02b0 100644
--- a/django/contrib/sessions/middleware.py
+++ b/django/contrib/sessions/middleware.py
@@ -42,6 +42,8 @@ class SessionMiddleware(MiddlewareMixin):
                 settings.SESSION_COOKIE_NAME,
                 path=settings.SESSION_COOKIE_PATH,
                 domain=settings.SESSION_COOKIE_DOMAIN,
+                samesite=settings.SESSION_COOKIE_SAMESITE,
+                secure=settings.SESSION_COOKIE_SECURE or None,
             )
             patch_vary_headers(response, ('Cookie',))
         else:
diff --git a/django/http/response.py b/django/http/response.py
index e00bcacefb..d2d9c23ca6 100644
--- a/django/http/response.py
+++ b/django/http/response.py
@@ -210,13 +210,15 @@ class HttpResponseBase:
         value = signing.get_cookie_signer(salt=key + salt).sign(value)
         return self.set_cookie(key, value, **kwargs)
 
-    def delete_cookie(self, key, path='/', domain=None):
+    def delete_cookie(self, key, path='/', domain=None, samesite=None, secure=None):
         # Most browsers ignore the Set-Cookie header if the cookie name starts
         # with __Host- or __Secure- and the cookie doesn't use the secure flag.
-        secure = key.startswith(('__Secure-', '__Host-'))
+        if secure is None:
+            secure = key.startswith(('__Secure-', '__Host-'))
         self.set_cookie(
             key, max_age=0, path=path, domain=domain, secure=secure,
             expires='Thu, 01 Jan 1970 00:00:00 GMT',
+            samesite=samesite,
         )
 
     # Common methods used by subclasses

```
