from pathlib import Path
import re

path = Path('index.html')
text = path.read_text(encoding='utf-8')

# Tribulus: replace supplement bottle-style image with raw plant/fruit photography.
text = text.replace(
    'https://commons.wikimedia.org/wiki/Special:Redirect/file/Tribulus_Terrestris.jpg',
    'https://commons.wikimedia.org/wiki/Special:Redirect/file/Tribulus_terrestris_fruit.jpg'
)
text = text.replace(
    'alt="Tribulus terrestris plant"',
    'alt="Buah mentah Tribulus terrestris pada tumbuhan"'
)
text = text.replace(
    '<small class="ing-credit">Photo: <a href="https://commons.wikimedia.org/wiki/File:Tribulus_Terrestris.jpg" target="_blank" rel="noopener">Carlosgraal / Wikimedia Commons</a></small>',
    '<small class="ing-credit">Photo: <a href="https://commons.wikimedia.org/wiki/File:Tribulus_terrestris_fruit.jpg" target="_blank" rel="noopener">Hüseyin Cahid Doğan / Wikimedia Commons</a></small>'
)

# Maltodextrin: use a clean raw-powder visual instead of labelled laboratory packaging.
text = text.replace(
    'https://commons.wikimedia.org/wiki/Special:Redirect/file/Maltodextrin_powder.jpg',
    'https://sgl08chemicals.com/cdn/shop/files/Maltodextrin.jpg?v=1708780496'
)
text = text.replace(
    'alt="Maltodextrin powder"',
    'alt="Serbuk maltodextrin dalam mangkuk"'
)
text = text.replace(
    '<small class="ing-credit">Photo: <a href="https://commons.wikimedia.org/wiki/File:Maltodextrin_powder.jpg" target="_blank" rel="noopener">Awkwafaba / Wikimedia Commons</a></small>',
    '<small class="ing-credit">Photo: <a href="https://sgl08chemicals.com/products/maltodextrin" target="_blank" rel="noopener">SGL08 Chemicals</a></small>'
)

# Remove the black 10-capsule / blister card entirely.
text, removed = re.subn(
    r'\n\s*<div class="ing-card ing-pack" style="background:var\(--navy\);">.*?</div>',
    '',
    text,
    count=1,
    flags=re.S,
)
if removed != 1:
    raise SystemExit(f'Expected to remove exactly one blister card, removed {removed}')

path.write_text(text, encoding='utf-8')
