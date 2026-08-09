(()=>{
const U='https://aytmfuevvoumobwfqptc.supabase.co';
const K='sb_publishable_Uol-itavAcZy4ciP3gbqJg_Ea9sw1TS';
const frame=document.getElementById('adminFrame');
if(!frame)return;

frame.addEventListener('load',()=>{
  try{
    const d=frame.contentDocument,w=frame.contentWindow;
    if(!d)return;

    // Desktop shell owns the only top bar. Hide the embedded page header and
    // return its vertical space to the active tab so every module can use the
    // full viewport beneath the shared navigation.
    if(window.matchMedia('(min-width:900px)').matches){
      if(!d.getElementById('testra-single-topbar-style')){
        const shell=d.createElement('style');
        shell.id='testra-single-topbar-style';
        shell.textContent='body>.top{display:none!important}.workspace{height:100vh!important}.reviewPage{height:100vh!important}.wrap{max-width:none!important;width:100%!important}.top+main.wrap,.top+.wrap{padding-top:18px!important}';
        d.head.appendChild(shell);
      }
    }

    if(!w?.supabase)return;
    const client=w.supabase.createClient(U,K);

    if(!d.getElementById('testra-delete-order-style')){
      const st=d.createElement('style');
      st.id='testra-delete-order-style';
      st.textContent='.testraDeleteOrder{margin-left:auto!important;background:#fff0ef!important;color:#d53d34!important;border:1px solid #ffd5d1!important}.testraDeleteOrder:hover{background:#ffe2df!important}.testraDeleteRow{display:flex;justify-content:flex-end;margin-top:8px}.order .testraDeleteOrder{position:relative;z-index:4}';
      d.head.appendChild(st);
    }

    async function removeOrder(card,btn){
      const id=card?.dataset?.id;
      if(!id)return;
      const no=card.querySelector('.orderNo')?.textContent?.trim()||'ini';
      const ok=w.confirm(`Delete order ${no}?\n\nTindakan ini akan memadam order dan rekod berkaitan. Tindakan ini tidak boleh dibatalkan.`);
      if(!ok)return;
      const old=btn.textContent;
      btn.disabled=true;
      btn.textContent='Deleting...';
      const {error}=await client.rpc('admin_delete_order',{p_order_id:id});
      if(error){
        btn.disabled=false;
        btn.textContent=old;
        w.alert('Delete gagal: '+error.message);
        return;
      }
      if(typeof w.loadOrders==='function'){
        try{await w.loadOrders();return}catch(_){ }
      }
      card.remove();
    }

    function enhance(){
      d.querySelectorAll('.order[data-id]').forEach(card=>{
        if(card.querySelector('.testraDeleteOrder'))return;
        let host=card.querySelector('.listActions');
        if(!host){host=d.createElement('div');host.className='testraDeleteRow';card.appendChild(host)}
        const btn=d.createElement('button');
        btn.type='button';
        btn.className='btn danger mini testraDeleteOrder';
        btn.textContent='🗑 Delete';
        btn.title='Delete order';
        btn.addEventListener('click',e=>{e.preventDefault();e.stopPropagation();removeOrder(card,btn)});
        host.appendChild(btn);
      });
    }

    enhance();
    new MutationObserver(enhance).observe(d.body,{childList:true,subtree:true});
  }catch(e){console.error('TESTRA admin enhancement failed',e)}
});
})();