from pathlib import Path
p=Path('index.html')
s=p.read_text(encoding='utf-8')
tag='<script src="pricing-live.js"></script>'
if tag not in s:
    s=s.replace('</body>',tag+'</body>',1)
p.write_text(s,encoding='utf-8')
