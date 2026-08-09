from pathlib import Path
import re

p=Path('index.html')
s=p.read_text(encoding='utf-8')

# Footer v2: remove old nav links, update email, and show real brand icons.
css='''
/* testra-footer-v2 */
footer{padding:52px 0 28px}.foot-links{display:none!important}.contact-main{justify-content:center;gap:12px;flex-wrap:wrap}.contact-main a{display:inline-flex;align-items:center;gap:10px}.footer-wa-icon{width:22px;height:22px;display:block}.social-row{justify-content:center;gap:14px;margin-top:22px}.social-row a{width:52px;height:52px;border-radius:50%;display:grid;place-items:center;background:#fff;border:1px solid var(--l);box-shadow:0 8px 22px #0a112812}.social-row svg{width:25px;height:25px;display:block}.footer-copy{text-align:center;margin-top:30px;color:var(--m)}
'''
if '/* testra-footer-v2 */' not in s:
    s=s.replace('</style>',css+'</style>',1)

# Remove the old footer nav row even if markup varies slightly.
s=re.sub(r'<div class="foot-links">.*?</div>','',s,count=1,flags=re.S)

# Update email everywhere in footer/page.
s=s.replace('hello@testra.my','testraman.worldwide@gmail.com')

# Replace contact/social area. Social hrefs intentionally remain placeholders until official URLs are supplied.
block='''<div class="contact-main"><a class="contact-pill" href="#" aria-label="WhatsApp TESTRA"><svg class="footer-wa-icon" viewBox="0 0 32 32" aria-hidden="true"><path fill="#25D366" d="M16 3a13 13 0 0 0-11.1 19.8L3.4 29l6.4-1.5A13 13 0 1 0 16 3Z"/><path fill="#fff" d="M22.8 18.7c-.4-.2-2.3-1.1-2.7-1.3-.4-.1-.7-.2-1 .2-.3.5-1 1.3-1.3 1.6-.2.3-.5.3-.9.1-2.5-1.2-4.1-2.2-5.8-5-.4-.7.4-.7 1.2-2.3.1-.3.1-.6 0-.8l-1.2-2.9c-.3-.7-.6-.6-1-.6h-.8c-.3 0-.8.1-1.2.6-.4.4-1.6 1.6-1.6 4s1.7 4.6 2 4.9c.2.3 3.4 5.2 8.3 7.3 3.1 1.3 4.3 1.4 5.8 1.2.9-.1 2.3-1 2.7-1.9.3-.9.3-1.7.2-1.9-.1-.2-.3-.3-.7-.5Z"/></svg><span>WhatsApp</span></a><a class="contact-pill" href="mailto:testraman.worldwide@gmail.com">testraman.worldwide@gmail.com</a></div><div class="social-row"><a href="#" aria-label="TikTok"><svg viewBox="0 0 24 24" aria-hidden="true"><path fill="#000" d="M14.2 3h3.1c.3 1.7 1.3 3 2.9 3.7v3.1a8.4 8.4 0 0 1-2.9-.7v6.2a6.3 6.3 0 1 1-5.4-6.2v3.2a3.2 3.2 0 1 0 2.3 3V3Z"/></svg></a><a href="#" aria-label="Instagram"><svg viewBox="0 0 24 24" aria-hidden="true"><defs><linearGradient id="ig" x1="0" y1="1" x2="1" y2="0"><stop stop-color="#FFD600"/><stop offset=".45" stop-color="#FF0069"/><stop offset="1" stop-color="#7638FA"/></linearGradient></defs><rect x="3" y="3" width="18" height="18" rx="5" fill="url(#ig)"/><circle cx="12" cy="12" r="4" fill="none" stroke="#fff" stroke-width="1.8"/><circle cx="17.4" cy="6.8" r="1.1" fill="#fff"/></svg></a><a href="#" aria-label="Facebook"><svg viewBox="0 0 24 24" aria-hidden="true"><circle cx="12" cy="12" r="10" fill="#1877F2"/><path fill="#fff" d="M13.5 21v-8h2.7l.4-3h-3.1V8.1c0-.9.3-1.5 1.6-1.5h1.7V3.9c-.3 0-1.3-.1-2.5-.1-2.5 0-4.2 1.5-4.2 4.3V10H7.3v3h2.8v8h3.4Z"/></svg></a></div>'''

# Replace existing contact-main + social-row as one region where possible.
pat=r'<div class="contact-main">.*?</div>\s*<div class="social-row">.*?</div>'
s,n=re.subn(pat,block,s,count=1,flags=re.S)
if n!=1:
    # Fallback: replace each independently.
    s,n1=re.subn(r'<div class="contact-main">.*?</div>',block,s,count=1,flags=re.S)
    if n1!=1: raise SystemExit('footer contact block not found')
    s=re.sub(r'<div class="social-row">.*?</div>','',s,count=1,flags=re.S)

p.write_text(s,encoding='utf-8')
