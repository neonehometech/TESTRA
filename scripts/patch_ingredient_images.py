from pathlib import Path
import re

path = Path('index.html')
text = path.read_text(encoding='utf-8')

css_marker = "  @media(max-width:760px){.ing-grid{grid-template-columns:1fr 1fr;}}"
css_addition = '''  @media(max-width:760px){.ing-grid{grid-template-columns:1fr 1fr;}}
  .ing-card{padding:0;overflow:hidden;text-align:left;display:flex;flex-direction:column;}
  .ing-photo{position:relative;height:150px;overflow:hidden;background:#eef0f7;}
  .ing-photo img{width:100%;height:100%;object-fit:cover;transition:transform .35s ease;}
  .ing-card:hover .ing-photo img{transform:scale(1.04);}
  .ing-body{padding:18px 18px 20px;}
  .ing-card h4{margin-bottom:6px;}
  .ing-credit{display:block;margin-top:10px;font-size:9px;line-height:1.35;color:#9297ad;}
  .ing-credit a{color:inherit;text-decoration:underline;text-underline-offset:2px;}
  .ing-pack{padding:24px 20px;text-align:center;justify-content:center;min-height:100%;}
  @media(max-width:760px){
    .ing-photo{height:118px;}
    .ing-body{padding:14px 14px 16px;}
    .ing-card h4{font-size:15px;}
    .ing-card p{font-size:12px;}
  }'''

if '.ing-photo{' not in text:
    if css_marker not in text:
        raise SystemExit('Ingredient CSS marker not found')
    text = text.replace(css_marker, css_addition, 1)

new_grid = '''<div class="ing-grid">
      <div class="ing-card">
        <div class="ing-photo"><img loading="lazy" src="https://commons.wikimedia.org/wiki/Special:Redirect/file/Tongkat_Ali_(Eurycoma_longifolia).jpg" alt="Tongkat Ali (Eurycoma longifolia)"></div>
        <div class="ing-body"><h4>Tongkat Ali</h4><p><span data-lang="bm">Herba tradisional popular untuk lelaki</span><span data-lang="en">Popular traditional herb for men</span></p><small class="ing-credit">Photo: <a href="https://commons.wikimedia.org/wiki/File:Tongkat_Ali_(Eurycoma_longifolia).jpg" target="_blank" rel="noopener">Mokkie / Wikimedia Commons</a></small></div>
      </div>
      <div class="ing-card">
        <div class="ing-photo"><img loading="lazy" src="https://commons.wikimedia.org/wiki/Special:Redirect/file/Epimedium.jpg" alt="Epimedium plant"></div>
        <div class="ing-body"><h4>Epimedium</h4><p><span data-lang="bm">Dikenali dalam herba tradisional Asia</span><span data-lang="en">Known in traditional Asian herbalism</span></p><small class="ing-credit">Photo: <a href="https://commons.wikimedia.org/wiki/File:Epimedium.jpg" target="_blank" rel="noopener">Hans Bernhard / Wikimedia Commons</a></small></div>
      </div>
      <div class="ing-card">
        <div class="ing-photo"><img loading="lazy" src="https://commons.wikimedia.org/wiki/Special:Redirect/file/Tribulus_Terrestris.jpg" alt="Tribulus terrestris plant"></div>
        <div class="ing-body"><h4>Tribulus Terrestris</h4><p><span data-lang="bm">Herba yang digunakan secara tradisional</span><span data-lang="en">Herb used in traditional practice</span></p><small class="ing-credit">Photo: <a href="https://commons.wikimedia.org/wiki/File:Tribulus_Terrestris.jpg" target="_blank" rel="noopener">Carlosgraal / Wikimedia Commons</a></small></div>
      </div>
      <div class="ing-card">
        <div class="ing-photo"><img loading="lazy" src="https://commons.wikimedia.org/wiki/Special:Redirect/file/Morinda_citrifolia_(fruit).jpg" alt="Buah mengkudu (Morinda citrifolia)"></div>
        <div class="ing-body"><h4><span data-lang="bm">Ekstrak Mengkudu</span><span data-lang="en">Noni Extract</span></h4><p><span data-lang="bm">Buah tempatan dalam ubatan tradisional</span><span data-lang="en">Local fruit used in traditional medicine</span></p><small class="ing-credit">Photo: <a href="https://commons.wikimedia.org/wiki/File:Morinda_citrifolia_(fruit).jpg" target="_blank" rel="noopener">Wikimedia Commons</a></small></div>
      </div>
      <div class="ing-card">
        <div class="ing-photo"><img loading="lazy" src="https://commons.wikimedia.org/wiki/Special:Redirect/file/Rhinacanthus_nasutus.jpg" alt="Telunjuk Langit (Rhinacanthus nasutus)"></div>
        <div class="ing-body"><h4><span data-lang="bm">Ekstrak Telunjuk Langit</span><span data-lang="en">Rhinacanthus Extract</span></h4><p><span data-lang="bm">Herba tempatan tradisional</span><span data-lang="en">Local traditional herb</span></p><small class="ing-credit">Photo: <a href="https://commons.wikimedia.org/wiki/File:Rhinacanthus_nasutus.jpg" target="_blank" rel="noopener">Vinayaraj / Wikimedia Commons</a></small></div>
      </div>
      <div class="ing-card">
        <div class="ing-photo"><img loading="lazy" src="https://inaturalist-open-data.s3.amazonaws.com/photos/251144043/original.jpeg" alt="Ubi Jaga (Smilax myosotiflora)"></div>
        <div class="ing-body"><h4><span data-lang="bm">Ekstrak Ubi Jaga</span><span data-lang="en">Ubi Jaga Extract</span></h4><p><span data-lang="bm">Herba tradisional Melayu</span><span data-lang="en">Traditional Malay herb</span></p><small class="ing-credit">Photo: <a href="https://www.inaturalist.org/taxa/426681-Smilax-myosotiflora" target="_blank" rel="noopener">Smilax myosotiflora / iNaturalist</a></small></div>
      </div>
      <div class="ing-card">
        <div class="ing-photo"><img loading="lazy" src="https://commons.wikimedia.org/wiki/Special:Redirect/file/Maltodextrin_powder.jpg" alt="Maltodextrin powder"></div>
        <div class="ing-body"><h4>Maltodextrin</h4><p><span data-lang="bm">Bahan pembawa (carrier) dalam formula</span><span data-lang="en">Carrier ingredient in the formula</span></p><small class="ing-credit">Photo: <a href="https://commons.wikimedia.org/wiki/File:Maltodextrin_powder.jpg" target="_blank" rel="noopener">Awkwafaba / Wikimedia Commons</a></small></div>
      </div>
      <div class="ing-card ing-pack" style="background:var(--navy);">
        <h4 style="color:#fff;">10 <span data-lang="bm">Kapsul</span><span data-lang="en">Capsules</span></h4>
        <p style="color:rgba(255,255,255,0.6);"><span data-lang="bm">1 Blister setiap kotak</span><span data-lang="en">1 blister per box</span></p>
      </div>
    </div>
    '''

pattern = r'<div class="ing-grid">.*?(?=<div style="margin-top:24px)'
updated, count = re.subn(pattern, new_grid, text, count=1, flags=re.S)
if count != 1:
    raise SystemExit(f'Expected one ingredient grid, found {count}')

path.write_text(updated, encoding='utf-8')
