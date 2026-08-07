from pathlib import Path
p=Path('index.html')
s=p.read_text()
if 'https://cdn.jsdelivr.net/npm/@supabase/supabase-js@2' not in s:
    s=s.replace('</head>','<script src="https://cdn.jsdelivr.net/npm/@supabase/supabase-js@2"></script>\n</head>')
start=s.index('    <div class="testi-grid">', s.index('<section class="testi" id="testimoni">'))
end=s.index('    </div>\n  </div>\n</section>', start)
replacement='''    <div class="testi-grid" id="testimonialGrid">\n      <div class="testi-card"><p class="quote"><span data-lang="bm">Memuatkan review pelanggan...</span><span data-lang="en">Loading customer reviews...</span></p></div>\n'''
s=s[:start]+replacement+s[end:]
needle="  document.querySelectorAll('.lang-toggle button').forEach(btn=>{"
loader='''  const reviewSb = supabase.createClient('https://aytmfuevvoumobwfqptc.supabase.co','sb_publishable_Uol-itavAcZy4ciP3gbqJg_Ea9sw1TS');\n  const esc = v => String(v ?? '').replace(/[&<>\"']/g, c => ({'&':'&amp;','<':'&lt;','>':'&gt;','\"':'&quot;',"'":'&#39;'}[c]));\n  async function loadTestimonials(){\n    const grid=document.getElementById('testimonialGrid');\n    const {data,error}=await reviewSb.from('reviews').select('customer_name,rating,comment,created_at').eq('is_published',true).order('created_at',{ascending:false}).limit(6);\n    if(error){ console.error(error); grid.innerHTML='<div class="testi-card"><p class="quote">Review belum dapat dimuatkan.</p></div>'; return; }\n    if(!data || !data.length){ grid.innerHTML='<div class="testi-card"><p class="quote"><span data-lang="bm">Belum ada review pelanggan yang diterbitkan.</span><span data-lang="en">No customer reviews published yet.</span></p></div>'; return; }\n    grid.innerHTML=data.map(r=>`<div class="testi-card"><div class="stars">${'★'.repeat(r.rating)}${'☆'.repeat(5-r.rating)}</div><p class="quote">“${esc(r.comment||'')}”</p><div class="testi-who"><div class="testi-avatar"></div><div><span>${esc(r.customer_name)}</span><small data-lang="bm">Pembeli Disahkan</small><small data-lang="en">Verified Buyer</small></div></div></div>`).join('');\n  }\n  loadTestimonials();\n\n'''
s=s.replace(needle,loader+needle)
p.write_text(s)
