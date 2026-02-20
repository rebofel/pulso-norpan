"""Clean up footer logo styling."""
import os

p = r'd:\GITHUB\recursos-humanos-norpan\docs\propuesta-pulso-norpan.html'
with open(p, 'r', encoding='utf-8') as f:
    h = f.read()

old = 'style="width:160px; opacity:0.8; filter: brightness(1.2);"'
new = 'style="width:160px;"'
h = h.replace(old, new)

with open(p, 'w', encoding='utf-8') as f:
    f.write(h)
print('Fixed footer logo style')
