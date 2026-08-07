from pathlib import Path
import re

path = Path("index.html")
text = path.read_text(encoding="utf-8")

replacement = '''<section class="problem" id="masalah">
  <div class="wrap">
    <div class="section-head">
      <div class="eyebrow-sm"><span data-lang="bm">HILANG KEYAKINAN?</span><span data-lang="en">LOST CONFIDENCE?</span></div>
      <h2><span data-lang="bm">Tanda-tanda lelaki moden yang memerlukan sokongan:</span><span data-lang="en">Signs modern men may need support:</span></h2>
    </div>
    <div class="problem-grid">
      <div class="problem-card">
        <div class="num">01</div>
        <p><span data-lang="bm">Cepat rasa penat</span><span data-lang="en">Tired easily</span></p>
      </div>
      <div class="problem-card">
        <div class="num">02</div>
        <p><span data-lang="bm">Stamina harian makin menurun</span><span data-lang="en">Daily stamina is declining</span></p>
      </div>
      <div class="problem-card">
        <div class="num">03</div>
        <p><span data-lang="bm">Fokus dan mood kurang konsisten</span><span data-lang="en">Focus and mood are less consistent</span></p>
      </div>
      <div class="problem-card">
        <div class="num">04</div>
        <p><span data-lang="bm">Tekanan hidup mula mengganggu keyakinan</span><span data-lang="en">Life pressures begin to affect confidence</span></p>
      </div>
    </div>
  </div>
</section>'''

pattern = r'<section class="problem" id="masalah">.*?</section>'
updated, count = re.subn(pattern, replacement, text, count=1, flags=re.S)
if count != 1:
    raise SystemExit(f"Expected exactly one problem section, found {count}")

path.write_text(updated, encoding="utf-8")
print("Updated TESTRA problem section")
