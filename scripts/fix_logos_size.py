"""Fix CTA logo size to match cover."""
import os

p = r'd:\GITHUB\recursos-humanos-norpan\docs\propuesta-pulso-norpan.html'
with open(p, 'r', encoding='utf-8') as f:
    h = f.read()

# CTA logo: was width:180px, change to height-based like cover
h = h.replace(
    'class="cover-logo" style="display:block; margin:0 auto 40px; width:180px;"',
    'class="cover-logo" style="display:block; margin:0 auto 36px; height:40px; width:auto;"'
)

# Footer logo: was width:160px
h = h.replace(
    'class="footer-logo" style="width:160px;"',
    'class="footer-logo" style="height:32px; width:auto; opacity:0.7;"'
)

with open(p, 'w', encoding='utf-8') as f:
    f.write(h)
print('Fixed CTA and footer logo sizes')
