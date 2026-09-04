# V5.2: patterns adapted from the 21st.dev survey (vanilla re-implementations). Run from bazoglu-v5: python scripts/patch-v52.py
import io
p = "index.html"
s = io.open(p, encoding="utf-8").read()

def rep(old, new, count=1):
    global s
    assert old in s, old[:60]
    s = s.replace(old, new, count)

# ---------- CSS ----------
css = """
/* v5.2: 21st.dev adaptations */
.scrollbar{position:fixed;top:0;left:0;right:0;height:3px;z-index:60;background:var(--yellow);transform:scaleX(0);transform-origin:left;pointer-events:none}
.ws{display:inline-block;will-change:transform,opacity,filter}
.words:not(.is-in) .ws{opacity:0;transform:translateY(10px);filter:blur(10px)}
.words.is-in .ws{opacity:1;transform:none;filter:blur(0);transition:opacity .5s ease-out,transform .5s ease-out,filter .5s ease-out;transition-delay:var(--wd,0s)}
.tabs,.modes{position:relative}
.tabs button,.modes button{border-bottom-color:transparent !important}
.tabs .ind,.modes .ind{position:absolute;bottom:-1px;height:3px;background:var(--yellow);transition:left .35s var(--ease),width .35s var(--ease);pointer-events:none}
.ticker{-webkit-mask-image:linear-gradient(90deg,transparent,#000 8%,#000 92%,transparent);mask-image:linear-gradient(90deg,transparent,#000 8%,#000 92%,transparent)}
.ticker:hover .ticker-track{animation-play-state:running;animation-duration:calc(var(--tick-dur,40s) * 2.5)}
.rail-item img,.cell img{transition:transform .45s var(--ease)}
.rail-item:hover img{transform:translateY(-8px) scale(1.04)}
.cell:hover img{transform:scale(1.04)}
.rail-item{position:relative}
.rail-item::after{content:"";position:absolute;left:0;right:0;bottom:0;height:3px;background:var(--yellow);transform:scaleX(0);transform-origin:left;transition:transform .35s var(--ease)}
.rail-item:hover::after{transform:scaleX(1)}
.tlink{text-decoration:none;background-image:linear-gradient(currentColor,currentColor);background-repeat:no-repeat;background-size:100% 1px;background-position:0 100%;padding-bottom:3px;transition:background-size .3s var(--ease)}
.tlink:hover{text-decoration:none;background-size:100% 2px}
.tlink.wipe{background-size:0 2px}
.tlink.wipe:hover,.tlink.wipe:focus-visible{background-size:100% 2px}
.btn{will-change:transform}
.price b{font-variant-numeric:tabular-nums}
.sss{padding:0 0 112px}
.sss h2{padding-top:96px}
.faq{margin-top:40px;border-top:1px solid var(--line)}
.faq details{border-bottom:1px solid var(--line)}
.faq summary{list-style:none;cursor:pointer;display:flex;align-items:center;justify-content:space-between;gap:24px;padding:24px 0;font:700 24px/1.15 var(--fd);color:var(--ink)}
.faq summary::-webkit-details-marker{display:none}
.faq summary i{flex:none;width:28px;height:28px;position:relative;border:1px solid var(--ink)}
.faq summary i::before,.faq summary i::after{content:"";position:absolute;background:var(--ink);left:50%;top:50%;transform:translate(-50%,-50%)}
.faq summary i::before{width:12px;height:1.5px}
.faq summary i::after{width:1.5px;height:12px;transition:transform .3s var(--ease)}
.faq details[open] summary i::after{transform:translate(-50%,-50%) rotate(90deg)}
.faq details[open] summary{color:var(--ink)}
.faq .a{overflow:hidden;height:0;transition:height .4s var(--ease)}
.faq .a p{padding:0 44px 24px 0;color:var(--ink-soft);max-width:70ch}
.faq details[open] summary::before{content:"";position:absolute;left:-16px;width:3px;height:28px;background:var(--yellow)}
.faq details{position:relative}
.fab{position:fixed;right:16px;bottom:16px;z-index:45;width:56px;height:56px;background:var(--yellow);border:1px solid var(--ink);display:none;align-items:center;justify-content:center;opacity:0;transform:translateY(12px);transition:opacity .3s,transform .3s var(--ease)}
.fab svg{width:26px;height:26px}
.fab.is-on{opacity:1;transform:none}
@media (max-width:820px){.fab{display:flex}}
@media (prefers-reduced-motion:reduce){
  .words:not(.is-in) .ws{opacity:1;transform:none;filter:none}
  .ticker:hover .ticker-track{animation:none !important}
}
"""
rep("/* reveal */", css + "\n/* reveal */")

# tabs/modes underline moved to the indicator element
rep(".tabs button[aria-selected=\"true\"]{border-bottom-color:var(--yellow)}", ".tabs button[aria-selected=\"true\"]{color:var(--white)}")
rep(".modes button[aria-selected=\"true\"]{border-bottom-color:var(--yellow)}", ".modes button[aria-selected=\"true\"]{color:var(--ink)}")

# ---------- HTML ----------
rep('<header class="nav" id="top">', '<div class="scrollbar" id="scrollbar" aria-hidden="true"></div>\n<header class="nav" id="top">')

rep('<h1>Michelin\'in Gaziantep\'teki adresi.</h1>', '<h1 class="words">Michelin\'in Gaziantep\'teki adresi.</h1>')
for t in ['<h2 class="rv">Lastiğinin yanında yazıyor.</h2>', '<h2 class="rv">Her seri. Her ebat.</h2>', '<h2 class="rv">Hizmetler</h2>', '<h2 class="rv">Randevu WhatsApp\'tan.</h2>', '<h2 class="rv">İnönü ve Küsget.</h2>']:
    rep(t, t.replace('class="rv"', 'class="words"'))

rep('<div class="tabs" role="tablist" aria-label="Lastik türü">', '<div class="tabs" role="tablist" aria-label="Lastik türü">\n    <span class="ind" aria-hidden="true"></span>')
rep('<div class="modes" role="tablist" aria-label="Arama yolu">', '<div class="modes" role="tablist" aria-label="Arama yolu">\n          <span class="ind" aria-hidden="true"></span>')

faq = '''
<section class="light sss" id="sss">
  <div class="wrap">
    <h2 class="words">Sık sorulanlar</h2>
    <div class="faq">
      <details><summary>4 lastik alınca montaj gerçekten dahil mi?<i></i></summary><div class="a"><p>Evet. 4 Michelin alana söküm, takma, balans ve sibop dahil, ayrıca ücret yok.</p></div></details>
      <details><summary>Fiyatlar KDV dahil mi, güncel mi?<i></i></summary><div class="a"><p>Sitedeki fiyatlar Eylül 2026 Michelin liste fiyatıdır, KDV dahil ve lastik başınadır. Kampanya ve stok için WhatsApp'tan yazın.</p></div></details>
      <details><summary>Randevu şart mı?<i></i></summary><div class="a"><p>Lastik değişimi, rot-balans ve lastik oteli için randevu alın, WhatsApp yeterli. Lastik tamiri için randevu gerekmez. Randevu saatleri 08:00-18:00, iki şubede de.</p></div></details>
      <details><summary>Aradığım ebat stokta yoksa?<i></i></summary><div class="a"><p>Michelin'in tüm binek, SUV, 4x4 ve hafif ticari serilerini her ebatta satıyoruz. Stokta yoksa bir günde getiriyoruz.</p></div></details>
      <details><summary>Lastik oteli nedir?<i></i></summary><div class="a"><p>Mevsimlik lastikleriniz bizde saklanır, etiketli ve kuru. Mevsim değişiminde randevuyla takılır.</p></div></details>
      <details><summary>Hafif ticari araçta hangi ebadı seçmeliyim?<i></i></summary><div class="a"><p>Ebadın sonunda C varsa, örnek 205/65 R16C, ölçü bulucuda C düğmesine basın. Emin değilseniz lastiğin yan yüzüne bakın ya da aracınızı seçin.</p></div></details>
      <details><summary>Kamyon ve ağır vasıta lastiği var mı?<i></i></summary><div class="a"><p>Var. Ebat, uygulama ve aks pozisyonuna göre WhatsApp'tan yazın.</p></div></details>
    </div>
  </div>
</section>

<section class="randevu" id="randevu">'''
rep('\n<section class="randevu" id="randevu">', faq)

fab = '''<a class="fab" id="fab" href="https://wa.me/905331433270" data-wa="Merhaba, Michelin lastik için bilgi almak istiyorum." target="_blank" rel="noopener" aria-label="WhatsApp'tan yaz">
  <svg viewBox="0 0 24 24" aria-hidden="true"><path fill="#121212" d="M12 2a10 10 0 0 0-8.6 15.1L2 22l5.1-1.3A10 10 0 1 0 12 2Zm0 1.8a8.2 8.2 0 1 1-4.2 15.2l-.3-.2-3 .8.8-2.9-.2-.3A8.2 8.2 0 0 1 12 3.8Zm-3.3 4.4c-.2 0-.5 0-.7.3-.3.3-1 1-1 2.3s1 2.7 1.2 2.9c.1.2 2 3.1 4.9 4.3 2.4 1 2.9.8 3.4.7.5 0 1.7-.7 1.9-1.4.2-.7.2-1.2.2-1.4-.1-.1-.3-.2-.6-.3l-2-1c-.3-.1-.5-.1-.7.1l-.9 1.1c-.2.2-.3.2-.6.1-.3-.1-1.2-.4-2.3-1.4-.9-.8-1.4-1.7-1.6-2-.2-.3 0-.4.1-.6l.4-.5.3-.5c.1-.2 0-.4 0-.5l-.9-2.1c-.2-.5-.4-.5-.6-.5h-.5Z"/></svg>
</a>
<script>'''
rep('\n<script>\n(function(){', '\n' + fab + '\n(function(){')

# nav: add FAQ to overlay only (desktop nav stays 5 links)
rep('<a class="big" href="#subeler">Şubeler</a>', '<a class="big" href="#subeler">Şubeler</a>\n  <a class="big" href="#sss">Sık sorulanlar</a>')

# ---------- JS ----------
# 1. scroll progress + fab in the scroll handler
rep('''  function onScroll(){
    onScrollNav();''', '''  var bar = document.getElementById("scrollbar"), fab = document.getElementById("fab");
  function onScrollExtras(){
    var max = document.documentElement.scrollHeight - window.innerHeight;
    bar.style.transform = "scaleX(" + (max > 0 ? Math.min(1, window.scrollY / max) : 0).toFixed(4) + ")";
    fab.classList.toggle("is-on", window.scrollY > window.innerHeight * 0.6);
  }
  onScrollExtras();
  function onScroll(){
    onScrollNav(); onScrollExtras();''')

# 2. words stagger: split headings, observe
rep('''  /* Reveal */
  var io = new IntersectionObserver(function(entries){''', '''  /* Words stagger (21st.dev "Words Stagger": blur 10px, y 10px, 0.5s ease-out, stagger) */
  document.querySelectorAll(".words").forEach(function(h){
    var words = h.textContent.trim().split(/\\s+/);
    h.textContent = "";
    words.forEach(function(w, i){
      var sp = document.createElement("span"); sp.className = "ws"; sp.textContent = w; sp.style.setProperty("--wd", (i * 0.07).toFixed(2) + "s");
      h.appendChild(sp); if (i < words.length - 1) h.appendChild(document.createTextNode(" "));
    });
  });
  var h1 = document.querySelector("h1.words");
  requestAnimationFrame(function(){ requestAnimationFrame(function(){ h1.classList.add("is-in"); }); });

  /* Reveal */
  var io = new IntersectionObserver(function(entries){''')
rep('''    (scope || document).querySelectorAll(".rv:not(.is-in), .branch:not(.is-in)").forEach(function(el, i){''',
    '''    (scope || document).querySelectorAll(".rv:not(.is-in), .branch:not(.is-in), h2.words:not(.is-in)").forEach(function(el, i){''')

# 3. count-up on prices (21st.dev "Count Up": tween to target when in view, tabular nums)
rep('''  /* Size finder */''', '''  /* Count up (21st.dev "Count Up" adapted: ease-out tween, thousands separator, starts in view) */
  var cio = new IntersectionObserver(function(entries){
    entries.forEach(function(e){
      if (!e.isIntersecting) return;
      cio.unobserve(e.target);
      var el = e.target, to = +el.getAttribute("data-to"), suffix = el.getAttribute("data-suffix") || "";
      if (reduced || !to){ return; }
      var t0 = performance.now(), dur = 900;
      function step(now){
        var t = Math.min(1, (now - t0) / dur), k = 1 - Math.pow(1 - t, 3);
        el.textContent = fmt.format(Math.round(to * k)) + suffix;
        if (t < 1) requestAnimationFrame(step);
      }
      requestAnimationFrame(step);
    });
  }, { threshold: 0 });
  function countUp(el){ cio.observe(el); }

  /* Size finder */''')
# price markup: wrap the amount in <b data-to>
rep('''          price.innerHTML = TL(h.size.price) + (many ? "<span style=\\"font:400 16px/1 var(--fb)\\">'den</span>" : "") +
            "<small>Lastik başına, KDV dahil. 4 adet " + TL(h.size.price * 4) + ", söküm, takma, balans ve sibop dahil.</small>";
          cell.appendChild(price);''', '''          price.innerHTML = "<b data-to=\\"" + h.size.price + "\\" data-suffix=\\" TL\\">" + TL(h.size.price) + "</b>" + (many ? "<span style=\\"font:400 16px/1 var(--fb)\\">'den</span>" : "") +
            "<small>Lastik başına, KDV dahil. 4 adet <b data-to=\\"" + (h.size.price * 4) + "\\" data-suffix=\\" TL\\">" + TL(h.size.price * 4) + "</b>, söküm, takma, balans ve sibop dahil.</small>";
          cell.appendChild(price);
          price.querySelectorAll("b[data-to]").forEach(countUp);''')

# 4. sliding tab indicator
rep('''  /* Tabs */''', '''  /* Sliding indicator (21st.dev "Underline Tabs" adapted) */
  function placeInd(list){
    var ind = list.querySelector(".ind"), act = list.querySelector('[aria-selected="true"]');
    if (!ind || !act) return;
    ind.style.left = (act.offsetLeft - list.scrollLeft) + "px"; ind.style.width = act.offsetWidth + "px";
  }
  var indLists = Array.prototype.slice.call(document.querySelectorAll(".tabs, .modes"));
  function placeAll(){ indLists.forEach(placeInd); }
  if (document.fonts && document.fonts.ready) document.fonts.ready.then(placeAll);
  window.addEventListener("resize", placeAll); placeAll();
  indLists.forEach(function(l){ l.addEventListener("scroll", function(){ placeInd(l); }); });

  /* Tabs */''')
rep('''      var r = activeRail(); r.scrollLeft = 0; observeReveal(r);''', '''      placeInd(t.parentElement);
      var r = activeRail(); r.scrollLeft = 0; observeReveal(r);''')
rep('''    panelSize.hidden = v; panelVehicle.hidden = !v;
    if (v) initVehicle();''', '''    panelSize.hidden = v; panelVehicle.hidden = !v;
    placeInd(modeSize.parentElement);
    if (v) initVehicle();''')

# 5. magnetic buttons + FAQ accordion + link wipe, appended before the closing of the IIFE
rep('''  vVersion.addEventListener("change", function(){
    var v = variants.filter(function(x){ return x.id === vVersion.value; })[0];
    showVariant(v || null);
  });
''', '''  vVersion.addEventListener("change", function(){
    var v = variants.filter(function(x){ return x.id === vVersion.value; })[0];
    showVariant(v || null);
  });

  /* Magnetic buttons (21st.dev "Magnetic" adapted: pull toward the cursor, spring back) */
  if (window.matchMedia("(pointer: fine)").matches && !reduced){
    document.querySelectorAll(".btn").forEach(function(b){
      b.addEventListener("pointermove", function(e){
        var r = b.getBoundingClientRect();
        var dx = (e.clientX - (r.left + r.width / 2)) / r.width, dy = (e.clientY - (r.top + r.height / 2)) / r.height;
        b.style.transition = "transform .15s ease-out";
        b.style.transform = "translate(" + (dx * 8).toFixed(1) + "px," + (dy * 6).toFixed(1) + "px)";
      });
      b.addEventListener("pointerleave", function(){ b.style.transition = "transform .45s cubic-bezier(.16,1,.3,1)"; b.style.transform = ""; });
    });
  }

  /* FAQ accordion with animated height (21st.dev "Accordion" adapted to native details) */
  document.querySelectorAll(".faq details").forEach(function(d){
    var a = d.querySelector(".a"), sum = d.querySelector("summary");
    if (d.open) a.style.height = "auto";
    sum.addEventListener("click", function(e){
      e.preventDefault();
      if (d.open){
        a.style.height = a.scrollHeight + "px";
        requestAnimationFrame(function(){ a.style.height = "0px"; });
        a.addEventListener("transitionend", function done(){ a.removeEventListener("transitionend", done); d.open = false; }, { once: true });
        if (reduced){ a.style.height = "0px"; d.open = false; }
      } else {
        d.open = true; a.style.height = "0px";
        requestAnimationFrame(function(){ a.style.height = a.scrollHeight + "px"; });
        a.addEventListener("transitionend", function done(){ a.removeEventListener("transitionend", done); if (d.open) a.style.height = "auto"; }, { once: true });
        if (reduced) a.style.height = "auto";
      }
    });
  });

  /* Link underline wipes in from the left for links inside lists and rails */
  document.querySelectorAll(".rail-item .tlink, .row .tlink, .branch .tlink").forEach(function(l){ l.classList.add("wipe"); });
''')

io.open(p, "w", encoding="utf-8", newline="\n").write(s)
print("patched", len(s))
