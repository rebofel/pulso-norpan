"""Embed logos as base64 data URIs into the HTML proposal."""
import base64
import os

root = r'd:\GITHUB\recursos-humanos-norpan'
html_path = os.path.join(root, 'docs', 'propuesta-pulso-norpan.html')

# Read logos as base64
with open(os.path.join(root, 'incba_claro.png'), 'rb') as f:
    claro_b64 = base64.b64encode(f.read()).decode()
with open(os.path.join(root, 'incba_oscuro.png'), 'rb') as f:
    oscuro_b64 = base64.b64encode(f.read()).decode()

print(f'claro: {len(claro_b64)} chars')
print(f'oscuro: {len(oscuro_b64)} chars')

# Read HTML
with open(html_path, 'r', encoding='utf-8') as f:
    html = f.read()

# Replace relative paths with data URIs
claro_uri = f'data:image/png;base64,{claro_b64}'
oscuro_uri = f'data:image/png;base64,{oscuro_b64}'

html = html.replace('src="../incba_claro.png"', f'src="{claro_uri}"')
html = html.replace('src="../incba_oscuro.png"', f'src="{oscuro_uri}"')

# Write back
with open(html_path, 'w', encoding='utf-8') as f:
    f.write(html)

size_kb = os.path.getsize(html_path) / 1024
print(f'HTML updated. Size: {size_kb:.0f} KB')
