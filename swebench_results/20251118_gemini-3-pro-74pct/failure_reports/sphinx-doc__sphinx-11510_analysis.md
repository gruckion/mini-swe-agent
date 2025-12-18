# Failure Analysis: sphinx-doc__sphinx-11510

## Basic Info
```
{
  "exit_status": "Submitted",
  "api_calls": 42,
  "cost": 0.6305802000000001
}
```

## Token Usage
- Max prompt tokens: 38104

## Files Modified in Submission
```
- sphinx/directives/other.py
- tox.ini
```

## Rule Violation Check

## Agent Reasoning About Tests
```
```

## Submission Diff (first 100 lines)
```diff
diff --git a/sphinx/directives/other.py b/sphinx/directives/other.py
index 19f7c0a8d..bf5d3c1a8 100644
--- a/sphinx/directives/other.py
+++ b/sphinx/directives/other.py
@@ -2,6 +2,7 @@ from __future__ import annotations
 
 import re
 from typing import TYPE_CHECKING, Any, cast
+from docutils import io, statemachine, utils
 
 from docutils import nodes
 from docutils.parsers.rst import directives
@@ -362,6 +363,7 @@ class Only(SphinxDirective):
             memo.section_level = surrounding_section_level
 
 
+
 class Include(BaseInclude, SphinxDirective):
     """
     Like the standard "Include" directive, but interprets absolute paths
@@ -376,8 +378,96 @@ class Include(BaseInclude, SphinxDirective):
         rel_filename, filename = self.env.relfn2path(self.arguments[0])
         self.arguments[0] = filename
         self.env.note_included(filename)
-        return super().run()
 
+        if 'literal' in self.options or 'code' in self.options or 'parser' in self.options:
+            return super().run()
+
+        if not self.state.document.settings.file_insertion_enabled:
+            raise self.warning('"%s" directive disabled.' % self.name)
+
+        encoding = self.options.get(
+            'encoding', self.state.document.settings.input_encoding)
+        e_handler = self.state.document.settings.input_encoding_error_handler
+
+        try:
+            include_file = io.FileInput(source_path=filename,
+                                        encoding=encoding,
+                                        error_handler=e_handler)
+        except UnicodeEncodeError:
+            raise self.severe(f'Problems with "{self.name}" directive path:\n'
+                              f'Cannot encode input file path "{filename}" '
+                              '(wrong locale?).')
+        except OSError as error:
+            raise self.severe(f'Problems with "{self.name}" directive '
+                              f'path:\n{io.error_string(error)}.')
+        else:
+            self.state.document.settings.record_dependencies.add(filename)
+
+        # Get to-be-included content
+        startline = self.options.get('start-line', None)
+        endline = self.options.get('end-line', None)
+        try:
+            if startline or (endline is not None):
+                lines = include_file.readlines()
+                rawtext = ''.join(lines[startline:endline])
+            else:
+                rawtext = include_file.read()
+        except UnicodeError as error:
+            raise self.severe(f'Problem with "{self.name}" directive:\n'
+                              + io.error_string(error))
+
+        # start-after/end-before
+        after_text = self.options.get('start-after', None)
+        if after_text:
+            after_index = rawtext.find(after_text)
+            if after_index < 0:
+                raise self.severe('Problem with "start-after" option of "%s" '
+                                  'directive:\nText not found.' % self.name)
+            rawtext = rawtext[after_index + len(after_text):]
+        before_text = self.options.get('end-before', None)
+        if before_text:
+            before_index = rawtext.find(before_text)
+            if before_index < 0:
+                raise self.severe('Problem with "end-before" option of "%s" '
+                                  'directive:\nText not found.' % self.name)
+            rawtext = rawtext[:before_index]
+
+        # emit "source-read" event
+        docname = self.env.path2doc(filename)
+        if docname:
+            arg = [rawtext]
+            self.env.events.emit('source-read', docname, arg)
+            rawtext = arg[0]
+
+        tab_width = self.options.get(
+            'tab-width', self.state.document.settings.tab_width)
+
+        include_lines = statemachine.string2lines(rawtext, tab_width,
+                                                  convert_whitespace=True)
+        for i, line in enumerate(include_lines):
+            if len(line) > self.state.document.settings.line_length_limit:
+                raise self.warning('"%s": line %d exceeds the'
+                                   ' line-length-limit.' % (filename, i + 1))
+
+        # Prevent circular inclusion
+        clip_options = (startline, endline, before_text, after_text)
+        include_log = self.state.document.include_log
+        if not include_log:
```
