from pathlib import Path
p=Path('index.html')
s=p.read_text()
if 'https://cdn.jsdelivr.net/npm/@supabase/supabase-js@2' not in s:
    s=s.replace('</head>','<script src="https://cdn.jsdelivr.net/npm/@supabase/supabase-js@2"></script>\n</head>')

# Replace the existing testimonial cards once; keep the section's established TESTRA styling.
if 'id="testimonialGrid"' not in s:
    sec=s.index('<section class="testi" id="testimoni">')
    start=s.index('    <div class="testi-grid">',sec)
    end=s.index('    </div>\n  </div>\n</section>',start)
    replacement='''    <div class="testi-grid" id="testimonialGrid">\n      <div class="testi-card"><p class="quote"><span data-lang="bm">Memuatkan pengalaman pelanggan...</span><span data-lang="en">Loading customer experiences...</span></p></div>\n'''
    s=s[:start]+replacement+s[end:]

# Install loader if it is not present yet.
if 'async function loadTestimonials()' not in s:
    needle="  document.querySelectorAll('.lang-toggle button').forEach(btn=>{"
    loader='''  const reviewSb = supabase.createClient('https://aytmfuevvoumobwfqptc.supabase.co','sb_publishable_Uol-itavAcZy4ciP3gbqJg_Ea9sw1TS');\n  const esc = v => String(v ?? '').replace(/[&<>\\"']/g, c => ({'&':'&amp;','<':'&lt;','>':'&gt;','\\"':'&quot;',"'":'&#39;'}[c]));\n  async function loadTestimonials(){\n    const grid=document.getElementById('testimonialGrid'); if(!grid)return;\n    const {data,error}=await reviewSb.from('reviews').select('customer_name,rating,comment,image_url,created_at').eq('is_published',true).order('created_at',{ascending:false}).limit(8);\n    if(error){console.error(error);grid.innerHTML='<div class="testi-card"><p class="quote">Review belum dapat dimuatkan.</p></div>';return;}\n    if(!data||!data.length){grid.innerHTML='<div class="testi-card"><p class="quote"><span data-lang="bm">Belum ada review pelanggan.</span><span data-lang="en">No customer reviews yet.</span></p></div>';return;}\n    grid.innerHTML=data.map(r=>`<div class="testi-card" style="overflow:hidden">${r.image_url?`<img src="${esc(r.image_url)}" alt="Review ${esc(r.customer_name)}" loading="lazy" style="width:100%;height:220px;object-fit:cover;border-radius:18px;margin-bottom:18px">`:''}<div class="stars">${'★'.repeat(Math.max(0,Math.min(5,r.rating||0)))}${'☆'.repeat(Math.max(0,5-(r.rating||0)))}</div><p class="quote">“${esc(r.comment||'')}”</p><div class="testi-who"><div class="testi-avatar"></div><div><span>${esc(r.customer_name)}</span></div></div></div>`).join('');\n  }\n  loadTestimonials();\n\n'''
    if needle not in s: raise SystemExit('language toggle anchor not found')
    s=s.replace(needle,loader+needle,1)
else:
    # Upgrade an earlier dynamic loader to include customer photos.
    s=s.replace("select('customer_name,rating,comment,created_at')","select('customer_name,rating,comment,image_url,created_at')")
    old="grid.innerHTML=data.map(r=>`<div class=\"testi-card\"><div class=\"stars\">${'★'.repeat(r.rating)}${'☆'.repeat(5-r.rating)}</div><p class=\"quote\">“${esc(r.comment||'')}”</p><div class=\"testi-who\"><div class=\"testi-avatar\"></div><div><span>${esc(r.customer_name)}</span><small data-lang=\"bm\">Pembeli Disahkan</small><small data-lang=\"en\">Verified Buyer</small></div></div></div>`).join('');"
    new="grid.innerHTML=data.map(r=>`<div class=\"testi-card\" style=\"overflow:hidden\">${r.image_url?`<img src=\"${esc(r.image_url)}\" alt=\"Review ${esc(r.customer_name)}\" loading=\"lazy\" style=\"width:100%;height:220px;object-fit:cover;border-radius:18px;margin-bottom:18px\">`:''}<div class=\"stars\">${'★'.repeat(r.rating)}${'☆'.repeat(5-r.rating)}</div><p class=\"quote\">“${esc(r.comment||'')}”</p><div class=\"testi-who\"><div class=\"testi-avatar\"></div><div><span>${esc(r.customer_name)}</span></div></div></div>`).join('');"
    s=s.replace(old,new)
p.write_text(s)
