# Failure Analysis: sympy__sympy-13878

## Basic Info
```
{
  "exit_status": "Submitted",
  "api_calls": 91,
  "cost": 1.0833224
}
```

## Token Usage
- Max prompt tokens: 44992

## Files Modified in Submission
```
- sympy/stats/crv_types.py
```

## Rule Violation Check

## Agent Reasoning About Tests
```
```

## Submission Diff (first 100 lines)
```diff
diff --git a/sympy/stats/crv_types.py b/sympy/stats/crv_types.py
index fff7da80ae..ca33b52383 100644
--- a/sympy/stats/crv_types.py
+++ b/sympy/stats/crv_types.py
@@ -47,7 +47,7 @@
 
 from sympy import (log, sqrt, pi, S, Dummy, Interval, sympify, gamma,
                    Piecewise, And, Eq, binomial, factorial, Sum, floor, Abs,
-                   Lambda, Basic, lowergamma, erf, erfc, I)
+                   Lambda, Basic, lowergamma, erf, erfc, I, uppergamma, asin, hyper)
 from sympy import beta as beta_fn
 from sympy import cos, exp, besseli
 from sympy.stats.crv import (SingleContinuousPSpace, SingleContinuousDistribution,
@@ -153,6 +153,9 @@ class ArcsinDistribution(SingleContinuousDistribution):
     def pdf(self, x):
         return 1/(pi*sqrt((x - self.a)*(self.b - x)))
 
+    def _cdf(self, x):
+        return 2/pi * asin(sqrt((x - self.a)/(self.b - self.a)))
+
 def Arcsin(name, a=0, b=1):
     r"""
     Create a Continuous Random Variable with an arcsin distribution.
@@ -671,6 +674,10 @@ def pdf(self, x):
         return a*p/x*((x/b)**(a*p)/(((x/b)**a + 1)**(p + 1)))
 
 
+    def _cdf(self, x):
+        p, a, b = self.p, self.a, self.b
+        return (1 + (x/b)**(-a))**(-p)
+
 def Dagum(name, p, a, b):
     r"""
     Create a continuous random variable with a Dagum distribution.
@@ -1042,6 +1049,10 @@ def pdf(self, x):
         a, s, m = self.a, self.s, self.m
         return a/s * ((x-m)/s)**(-1-a) * exp(-((x-m)/s)**(-a))
 
+    def _cdf(self, x):
+        a, s, m = self.a, self.s, self.m
+        return exp(-((x - m)/s)**(-a))
+
 def Frechet(name, a, s=1, m=0):
     r"""
     Create a continuous random variable with a Frechet distribution.
@@ -1108,6 +1119,10 @@ def pdf(self, x):
         k, theta = self.k, self.theta
         return x**(k - 1) * exp(-x/theta) / (gamma(k)*theta**k)
 
+    def _cdf(self, x):
+        k, theta = self.k, self.theta
+        return lowergamma(k, x/theta) / gamma(k)
+
     def sample(self):
         return random.gammavariate(self.k, self.theta)
 
@@ -1200,6 +1215,10 @@ def pdf(self, x):
         a, b = self.a, self.b
         return b**a/gamma(a) * x**(-a-1) * exp(-b/x)
 
+    def _cdf(self, x):
+        a, b = self.a, self.b
+        return uppergamma(a, b/x) / gamma(a)
+
 def GammaInverse(name, a, b):
     r"""
     Create a continuous random variable with an inverse Gamma distribution.
@@ -1385,6 +1404,10 @@ def pdf(self, x):
         a, b = self.a, self.b
         return a * b * x**(a-1) * (1-x**a)**(b-1)
 
+    def _cdf(self, x):
+        a, b = self.a, self.b
+        return 1 - (1 - x**a)**b
+
 def Kumaraswamy(name, a, b):
     r"""
     Create a Continuous Random Variable with a Kumaraswamy distribution.
@@ -1446,6 +1469,13 @@ def pdf(self, x):
         return 1/(2*b)*exp(-Abs(x - mu)/b)
 
 
+    def _cdf(self, x):
+        mu, b = self.mu, self.b
+        return Piecewise(
+            (S.Half * exp((x - mu)/b), x < mu),
+            (1 - S.Half * exp(-(x - mu)/b), True)
+        )
+
 def Laplace(name, mu, b):
     r"""
     Create a continuous random variable with a Laplace distribution.
@@ -1502,6 +1532,10 @@ def pdf(self, x):
         return exp(-(x - mu)/s)/(s*(1 + exp(-(x - mu)/s))**2)
 
 
+    def _cdf(self, x):
+        mu, s = self.mu, self.s
+        return 1 / (1 + exp(-(x - mu)/s))
+
```
