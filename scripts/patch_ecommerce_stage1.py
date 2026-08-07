from pathlib import Path

path = Path('index.html')
text = path.read_text(encoding='utf-8')

replacements = {
'''      <div class="pkg">\n        <div class="tag" data-lang="bm">1 Botol</div><div class="tag" data-lang="en">1 Bottle</div>\n        <div class="price">RM89</div>\n      </div>''': '''      <a class="pkg" href="checkout.html?package=TST-1" aria-label="Pilih pakej 1 botol">\n        <div class="tag" data-lang="bm">1 Botol</div><div class="tag" data-lang="en">1 Bottle</div>\n        <div class="price">RM89</div>\n      </a>''',
'''      <div class="pkg featured">\n        <div class="tag" data-lang="bm">3 Botol · Popular</div><div class="tag" data-lang="en">3 Bottles · Popular</div>\n        <div class="price">RM239</div>\n      </div>''': '''      <a class="pkg featured" href="checkout.html?package=TST-3" aria-label="Pilih pakej 3 botol">\n        <div class="tag" data-lang="bm">3 Botol · Popular</div><div class="tag" data-lang="en">3 Bottles · Popular</div>\n        <div class="price">RM239</div>\n      </a>''',
'''      <div class="pkg">\n        <div class="tag" data-lang="bm">5 Botol · Jimat</div><div class="tag" data-lang="en">5 Bottles · Best Value</div>\n        <div class="price">RM369</div>\n      </div>''': '''      <a class="pkg" href="checkout.html?package=TST-5" aria-label="Pilih pakej 5 botol">\n        <div class="tag" data-lang="bm">5 Botol · Jimat</div><div class="tag" data-lang="en">5 Bottles · Best Value</div>\n        <div class="price">RM369</div>\n      </a>''',
'''    <a href="#" class="btn btn-white">\n      <span data-lang="bm">Order Sekarang →</span><span data-lang="en">Order Now →</span>\n    </a>''': '''    <a href="checkout.html?package=TST-3" class="btn btn-white">\n      <span data-lang="bm">Order Sekarang →</span><span data-lang="en">Order Now →</span>\n    </a>'''
}

for old, new in replacements.items():
    if old not in text:
        raise SystemExit('Expected order-section block not found; refusing unsafe patch')
    text = text.replace(old, new, 1)

path.write_text(text, encoding='utf-8')
print('Patched TESTRA order section for checkout flow')
