# Failure Analysis: django__django-11848

## Basic Info
```
{
  "exit_status": "Submitted",
  "api_calls": 21,
  "cost": 0.35562800000000006
}
```

## Token Usage
- Max prompt tokens: 24008

## Files Modified in Submission
```
- django/utils/http.py
```

## Rule Violation Check

## Agent Reasoning About Tests
```
   The instructions say "MODIFY: Regular source code files ... DO NOT MODIFY: Tests".
```

## Submission Diff (first 100 lines)
```diff
diff --git a/django/utils/http.py b/django/utils/http.py
index 572cfb4347..5c44463e1b 100644
--- a/django/utils/http.py
+++ b/django/utils/http.py
@@ -176,10 +176,11 @@ def parse_http_date(date):
     try:
         year = int(m.group('year'))
         if year < 100:
-            if year < 70:
-                year += 2000
-            else:
-                year += 1900
+            current_year = datetime.datetime.now(datetime.timezone.utc).year
+            current_century = current_year - (current_year % 100)
+            year += current_century
+            if year - current_year > 50:
+                year -= 100
         month = MONTHS.index(m.group('mon').lower()) + 1
         day = int(m.group('day'))
         hour = int(m.group('hour'))

```
