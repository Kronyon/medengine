#!/usr/bin/env python3
"""v3.6.3: older MSCAA papers write 10 mL of 10% calcium gluconate; UK Kidney Association now says 30 mL. Show both."""
import pathlib
F = pathlib.Path(__file__).resolve().parents[1] / 'study.html'
s = F.read_text(encoding='utf-8')
for a, b in (("(gluconate 10% 30 mL, or chloride 10% 10 mL)", "(gluconate 10% 30 mL, or chloride 10% 10 mL; older papers write 10 mL of gluconate, pick it if that is the only calcium option)"),
             ("IV calcium gluconate 10% 30 mL first (protects heart)", "IV calcium gluconate 10% 30 mL first (older papers: 10 mL; protects heart)")):
    assert s.count(a) == 1, a
    s = s.replace(a, b)
F.write_text(s, encoding='utf-8')
print('ok')
