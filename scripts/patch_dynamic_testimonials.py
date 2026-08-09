from pathlib import Path
import re

p = Path('index.html')
s = p.read_text(encoding='utf-8')

# Supabase browser client.
if 'https://cdn.jsdelivr.net/npm/@supabase/supabase-js@2' not in s:
    s = s.replace('</head>', '<script src="https://cdn.jsdelivr.net/npm/@supabase/supabase-js@2"></script></head>', 1)

# Review section CSS. Mobile is one large swipe card with a peek of the next card.
css = r'''
/* testra-review-feed-v2 */
.testi{background:radial-gradient(circle at 88% 10%,#fff0e6 0,transparent 28%),radial-gradient(circle at 10% 88%,#eaf3ff 0,transparent 30%),#fff;padding:88px 0 104px;overflow:hidden}.testi .section-head{margin-bottom:32px}.testi .section-head h2{font-size:clamp(38px,5vw,58px);line-height:1.05;margin:10px 0 0;color:#0a1128}.testi-grid{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:20px}.testi-card{background:#fff;border:1px solid #e1e5ef;border-radius:28px;padding:24px;box-shadow:0 18px 48px rgba(10,17,40,.08);min-width:0}.testi-card.has-photo{padding:0;overflow:hidden}.testi-card .review-photo{width:100%;aspect-ratio:4/3;object-fit:cover;display:block;background:#f2f4fa}.testi-card.has-photo .review-body{padding:22px 24px 24px}.testi-card .stars{color:#ffb100;font-size:20px;letter-spacing:2px;line-height:1}.testi-card .quote{font-size:17px;line-height:1.65;color:#252a3e;margin:18px 0 22px}.testi-card .testi-who{display:flex;align-items:center;gap:11px}.testi-card .testi-avatar{width:38px;height:38px;border-radius:50%;background:linear-gradient(145deg,#1746ff,#0b2aa9);display:grid;place-items:center;color:#fff;font-weight:800;flex:0 0 auto}.testi-card .testi-name{font-weight:800;color:#0a1128}.testi-card .testi-date{font-size:11px;color:#8a90a4;margin-top:2px}.testi-empty{grid-column:1/-1;text-align:center;padding:32px;color:#6b7091;background:#f7f7fb;border-radius:24px;border:1px solid #e4e5f1}@media(max-width:900px){.testi-grid{grid-template-columns:repeat(2,minmax(0,1fr))}}@media(max-width:760px){.testi{padding:68px 0 82px}.testi .section-head{margin-bottom:26px}.testi-grid{display:flex;gap:14px;overflow-x:auto;scroll-snap-type:x mandatory;scroll-padding-left:18px;padding:4px 18px 18px;margin-left:-18px;margin-right:-18px;-webkit-overflow-scrolling:touch;scrollbar-width:none}.testi-grid::-webkit-scrollbar{display:none}.testi-card{flex:0 0 86%;scroll-snap-align:start;border-radius:26px;padding:22px}.testi-card.has-photo{padding:0}.testi-card.has-photo .review-body{padding:20px 22px 23px}.testi-card .quote{font-size:17px;line-height:1.6}.testi-empty{flex:0 0 92%;text-align:left}}
'''
if '/* testra-review-feed-v2 */' not in s:
    s = s.replace('</style>', css + '</style>', 1)

# Replace the complete legacy testimonial section, regardless of its old card contents.
section = '''<section class="testi" id="testimoni"><div class="wrap"><div class="section-head"><div class="eyebrow-sm"><span data-lang="bm">APA KATA MEREKA</span><span data-lang="en">WHAT THEY SAY</span></div><h2><span data-lang="bm">Pengalaman pelanggan.</span><span data-lang="en">Customer experiences.</span></h2></div><div class="testi-grid" id="testimonialGrid"><div class="testi-empty"><span data-lang="bm">Memuatkan review pelanggan...</span><span data-lang="en">Loading customer reviews...</span></div></div></div></section>'''
s, n = re.subn(r'<section class="testi" id="testimoni">.*?</section>', section, s, count=1, flags=re.S)
if n != 1:
    raise SystemExit('testimonial section not found exactly once')

# Remove any older injected review loader, then append the canonical loader.
s = re.sub(r'<script id="testra-review-loader">.*?</script>', '', s, flags=re.S)
loader = r'''<script id="testra-review-loader">
(()=>{
  const reviewSb=supabase.createClient('https://aytmfuevvoumobwfqptc.supabase.co','sb_publishable_Uol-itavAcZy4ciP3gbqJg_Ea9sw1TS');
  const esc=v=>String(v??'').replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
  const initials=v=>String(v||'?').trim().split(/\s+/).slice(0,2).map(x=>x[0]||'').join('').toUpperCase();
  const dateLabel=v=>{try{return new Intl.DateTimeFormat(document.body.classList.contains('lang-en')?'en-MY':'ms-MY',{day:'numeric',month:'short',year:'numeric'}).format(new Date(v))}catch(_){return ''}};
  async function loadTestimonials(){
    const grid=document.getElementById('testimonialGrid');if(!grid)return;
    const {data,error}=await reviewSb.from('reviews').select('customer_name,rating,comment,image_url,created_at').eq('is_published',true).order('created_at',{ascending:false}).limit(12);
    if(error){console.error('Review load failed',error);grid.innerHTML='<div class="testi-empty">Review belum dapat dimuatkan.</div>';return;}
    if(!data?.length){grid.innerHTML='<div class="testi-empty"><span data-lang="bm">Belum ada review pelanggan.</span><span data-lang="en">No customer reviews yet.</span></div>';return;}
    grid.innerHTML=data.map(r=>{const photo=r.image_url?`<img class="review-photo" src="${esc(r.image_url)}" alt="Review ${esc(r.customer_name)}" loading="lazy">`:'';const stars='★'.repeat(Math.max(0,Math.min(5,Number(r.rating)||0)))+'☆'.repeat(Math.max(0,5-(Number(r.rating)||0)));return `<article class="testi-card ${r.image_url?'has-photo':''}">${photo}<div class="review-body"><div class="stars" aria-label="${Number(r.rating)||0} daripada 5">${stars}</div><p class="quote">“${esc(r.comment||'')}”</p><div class="testi-who"><div class="testi-avatar">${esc(initials(r.customer_name))}</div><div><div class="testi-name">${esc(r.customer_name)}</div><div class="testi-date">${esc(dateLabel(r.created_at))}</div></div></div></div></article>`}).join('');
  }
  loadTestimonials();
})();
</script>'''
s = s.replace('</body>', loader + '</body>', 1)

p.write_text(s, encoding='utf-8')
