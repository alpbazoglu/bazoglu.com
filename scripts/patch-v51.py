# One-off patch: prices (Eylül 2026) + "Aracıma göre" vehicle mode. Run from bazoglu-v5: python scripts/patch-v51.py
import io, re
p = "index.html"
s = io.open(p, encoding="utf-8").read()

# ---------- CSS ----------
css_add = """.modes{display:flex;gap:28px;margin-bottom:24px;border-bottom:1px solid var(--line)}
.modes button{background:none;border:0;border-bottom:3px solid transparent;margin-bottom:-1px;padding:12px 0;font:600 16px/1 var(--fb);color:var(--ink);cursor:pointer}
.modes button[aria-selected="true"]{border-bottom-color:var(--yellow)}
.vgrid{display:grid;grid-template-columns:1fr 1fr;gap:16px}
.vgrid select{font:600 18px/1 var(--fb);height:56px;background-position:right 12px center}
.vgrid select:disabled{color:var(--ink-soft);border-color:var(--line);cursor:default}
.vresults{margin-top:20px;display:flex;flex-direction:column;gap:1px;background:var(--line);border:1px solid var(--line)}
.vresults:empty{display:none}
.vsize{display:flex;align-items:center;gap:16px;background:var(--card);border:0;border-left:3px solid transparent;padding:14px 16px;text-align:left;cursor:pointer;font:400 15px/1.3 var(--fb);color:var(--ink);width:100%}
.vsize b{font:700 30px/1 var(--fd)}
.vsize span{color:var(--ink-soft)}
.vsize:hover,.vsize[aria-pressed="true"]{background:var(--paper)}
.vsize[aria-pressed="true"]{border-left-color:var(--yellow)}
.vnote{background:var(--card);padding:14px 16px;color:var(--ink-soft);font-size:15px}
.vnote a{color:var(--ink)}
.results .sub{margin:-16px 0 24px;color:var(--ink-soft);font-size:15px}
.results .sub:empty{display:none}
.price{font:700 30px/1 var(--fd);color:var(--ink);margin-top:6px}
.price small{display:block;font:400 14px/1.4 var(--fb);color:var(--ink-soft);margin-top:6px}
.price.ask{font:400 15px/1.4 var(--fb);color:var(--ink-soft)}
.skus{margin:4px 0 0;padding:0;list-style:none;font-size:14px;color:var(--ink-soft)}
.skus li{display:flex;justify-content:space-between;gap:12px;border-top:1px solid var(--line);padding:4px 0}
.pricenote{margin-top:24px;font-size:14px;color:var(--ink-soft)}
"""
s = s.replace("/* lastikler */", css_add + "\n/* lastikler */", 1)
s = s.replace("  .finder-card{padding:20px}", "  .finder-card{padding:20px}\n  .vgrid{grid-template-columns:1fr}\n  .modes{gap:20px}", 1)

# ---------- hero ghost button -> vehicle mode ----------
s = s.replace('<a class="btn btn-ghost" href="https://wa.me/905331433270" data-wa="Merhaba, aracım için Michelin lastik fiyatı almak istiyorum. Araç: " target="_blank" rel="noopener">Aracını yaz, biz bulalım</a>',
              '<a class="btn btn-ghost" href="#olcu" data-mode="vehicle">Aracıma göre bul</a>', 1)
s = s.replace('<li><a href="#olcu">Ölçünü bul</a></li>', '<li><a href="#olcu">Ölçünü bul</a></li>\n        <li><a href="#olcu" data-mode="vehicle">Aracıma göre</a></li>', 1)

# ---------- finder markup ----------
old_form_start = s.index('      <form class="finder-card" id="finder" novalidate>')
old_form_end = s.index('      </form>', old_form_start) + len('      </form>')
new_form = '''      <form class="finder-card" id="finder" novalidate>
        <div class="modes" role="tablist" aria-label="Arama yolu">
          <button type="button" role="tab" id="modeSize" aria-selected="true" aria-controls="panelSize">Ölçüye göre</button>
          <button type="button" role="tab" id="modeVehicle" aria-selected="false" aria-controls="panelVehicle">Aracıma göre</button>
        </div>
        <div id="panelSize" role="tabpanel" aria-labelledby="modeSize">
          <div class="finder-row">
            <div class="field"><label for="selW">Genişlik</label><select id="selW" name="w"></select></div>
            <span class="sep" aria-hidden="true">/</span>
            <div class="field"><label for="selA">Kesit</label><select id="selA" name="a"></select></div>
            <span class="sep" aria-hidden="true">R</span>
            <div class="field"><label for="selR">Jant</label><select id="selR" name="r"></select></div>
            <button class="ctoggle" type="button" id="cToggle" aria-pressed="false" aria-label="C, hafif ticari ebat">C</button>
          </div>
          <button class="btn btn-yellow" type="submit" id="findBtn">Bu ebattaki Michelin'leri göster</button>
          <p class="finder-note" id="finderNote">Michelin'in tüm binek, SUV, 4x4 ve hafif ticari serilerini her ebatta satıyoruz. Fiyatlar Eylül 2026 listesi, KDV dahil.</p>
        </div>
        <div id="panelVehicle" role="tabpanel" aria-labelledby="modeVehicle" hidden>
          <div class="vgrid">
            <div class="field"><label for="vMake">Marka</label><select id="vMake"><option value="">Seçin</option></select></div>
            <div class="field"><label for="vModel">Model</label><select id="vModel" disabled><option value="">Seçin</option></select></div>
            <div class="field"><label for="vYear">Yıl</label><select id="vYear" disabled><option value="">Seçin</option></select></div>
            <div class="field" id="vVersionField" hidden><label for="vVersion">Versiyon / Motor</label><select id="vVersion"><option value="">Seçin</option></select></div>
          </div>
          <div id="vResults" class="vresults" aria-live="polite"></div>
          <p class="finder-note" id="vNote">Marka, model ve yılı seç; aracının fabrika ebadını gösterelim. Aracın listede yoksa WhatsApp'tan yaz, biz bulalım.</p>
        </div>
      </form>'''
s = s[:old_form_start] + new_form + s[old_form_end:]
s = s.replace('      <h3 id="resultsTitle">225/45 R18 için Michelin serileri</h3>\n      <div class="grid" id="resultsGrid"></div>',
              '      <h3 id="resultsTitle">225/45 R18 için Michelin serileri</h3>\n      <p class="sub" id="resultsSub"></p>\n      <div class="grid" id="resultsGrid"></div>\n      <p class="pricenote" id="priceNote"></p>', 1)

# ---------- JS: replace from "/* Size finder */" to "/* Tabs */" ----------
js_start = s.index("  /* Size finder */")
js_end = s.index("  /* Tabs */")
new_js = r'''  /* Size finder */
  var SEASON = { summer: "Yaz", allseason: "4 Mevsim", winter: "Kış" };
  var selW = document.getElementById("selW"), selA = document.getElementById("selA"), selR = document.getElementById("selR");
  var cToggle = document.getElementById("cToggle");
  var form = document.getElementById("finder");
  var grid = document.getElementById("resultsGrid");
  var title = document.getElementById("resultsTitle");
  var sub = document.getElementById("resultsSub");
  var note = document.getElementById("finderNote");
  var priceNote = document.getElementById("priceNote");
  var families = null;   /* catalog */
  var priceList = null;
  var index = {};        /* key -> [{family,size}] */
  var tree = {};         /* commercial -> width -> aspect -> rims */
  var pendingFamily = null;
  var vehicle = null;    /* { label, make, model, year } when the size came from a vehicle */
  var fmt = new Intl.NumberFormat("tr-TR");
  var TL = function(n){ return fmt.format(n) + " TL"; };
  var OE = /\*|\b(MO1?|MOE|AO1?|N[0-4]|N[A-G]0|VOL|T[0-2]|RO[12]|ZP|ACOUSTIC|SELFSEAL|POL|JLR|LR|MGT|K[12]|HN|HO|AR|AML|TPC|RG|OP|PE|GOE)\b/g;

  function key(w,a,r,c){ return w + "-" + a + "-" + r + (c ? "C" : ""); }
  function display(w,a,r,c){ return w + "/" + a + " R" + r + (c ? "C" : ""); }
  function parseKey(k){
    var m = /^(\d{3})-(\d{2,3})-(\d{2}(?:\.5)?)(C?)$/.exec(k || "");
    return m ? { w: +m[1], a: +m[2], r: +m[3], c: !!m[4] } : null;
  }
  function fill(sel, values, keep){
    var cur = keep !== undefined ? keep : sel.value;
    sel.innerHTML = "";
    values.forEach(function(v){ var o = document.createElement("option"); o.value = v; o.textContent = v; sel.appendChild(o); });
    if (values.indexOf(Number(cur)) !== -1) sel.value = cur;
    else if (values.indexOf(String(cur)) !== -1) sel.value = cur;
  }
  function isC(){ return cToggle.getAttribute("aria-pressed") === "true"; }
  function num(a,b){ return a - b; }

  function fillWidths(pref){
    var t = tree[isC() ? 1 : 0] || {};
    var ws = Object.keys(t).map(Number).sort(num);
    fill(selW, ws, pref !== undefined ? pref : selW.value);
    if (!selW.value && ws.length) selW.value = ws.indexOf(225) !== -1 ? 225 : ws[0];
  }
  function fillAspects(pref){
    var t = (tree[isC() ? 1 : 0] || {})[selW.value] || {};
    var as = Object.keys(t).map(Number).sort(num);
    fill(selA, as, pref !== undefined ? pref : selA.value);
    if (!selA.value && as.length) selA.value = as.indexOf(45) !== -1 ? 45 : as[0];
  }
  function fillRims(pref){
    var rs = (((tree[isC() ? 1 : 0] || {})[selW.value] || {})[selA.value] || []).slice().sort(num);
    fill(selR, rs, pref !== undefined ? pref : selR.value);
    if (!selR.value && rs.length) selR.value = rs.indexOf(18) !== -1 ? 18 : rs[0];
  }
  function setSize(w,a,r,c){
    cToggle.setAttribute("aria-pressed", String(!!c));
    fillWidths(w); fillAspects(a); fillRims(r);
  }
  function selectedSize(){ return { w: +selW.value, a: +selA.value, r: +selR.value, c: isC() }; }

  function skuLabel(sku){
    var marks = (sku.desc.match(OE) || []).filter(function(m, i, arr){ return arr.indexOf(m) === i; });
    var xl = /\bXL\b/.test(sku.desc) ? " XL" : "";
    return sku.spec + xl + (marks.length ? ", " + marks.join(" ") : "");
  }

  function render(sz){
    sz = sz || selectedSize();
    var disp = display(sz.w, sz.a, sz.r, sz.c);
    title.textContent = disp + " için Michelin serileri";
    sub.textContent = vehicle ? vehicle.label + " için fabrika ebadı." : "";
    grid.innerHTML = "";
    var hits = index[key(sz.w, sz.a, sz.r, sz.c)] || [];
    if (pendingFamily){
      hits = hits.slice().sort(function(x,y){ return (y.family.id === pendingFamily) - (x.family.id === pendingFamily); });
      pendingFamily = null;
    } else {
      hits = hits.slice().sort(function(x,y){ return (x.size.price || 1e9) - (y.size.price || 1e9); });
    }
    var forVehicle = vehicle ? " Aracım: " + vehicle.label + "." : "";
    if (!hits.length){
      var e = document.createElement("div");
      e.className = "cell empty";
      e.innerHTML = "<h3>Bu ebat listede yok. Yaz, bulalım.</h3><p class=\"meta\">" + disp + " için stok ve fiyatı WhatsApp'tan soralım.</p>";
      var l = document.createElement("a"); l.className = "tlink"; l.target = "_blank"; l.rel = "noopener";
      l.href = waHref("Merhaba, " + disp + " Michelin lastik fiyatı alabilir miyim?" + forVehicle); l.textContent = "WhatsApp'tan sor";
      e.appendChild(l); grid.appendChild(e);
    } else {
      hits.forEach(function(h){
        var cell = document.createElement("div"); cell.className = "cell";
        if (h.family.image){
          var img = document.createElement("img");
          img.src = "assets/" + h.family.id + "-800.webp"; img.width = 800; img.height = 718; img.loading = "lazy";
          img.alt = "Michelin " + h.family.name + " lastik"; cell.appendChild(img);
        }
        var h3 = document.createElement("h3"); h3.textContent = h.family.name; cell.appendChild(h3);
        var meta = document.createElement("p"); meta.className = "meta";
        var parts = [SEASON[h.family.season] || h.family.season];
        if (h.size.specs && h.size.specs.length) parts.push(h.size.specs.join(", "));
        meta.textContent = parts.join(", "); cell.appendChild(meta);
        var price = document.createElement("p");
        if (h.size.price){
          price.className = "price";
          var many = h.size.skus.length > 1 && h.size.skus[h.size.skus.length - 1].price !== h.size.price;
          price.innerHTML = TL(h.size.price) + (many ? "<span style=\"font:400 16px/1 var(--fb)\">'den</span>" : "") +
            "<small>Lastik başına, KDV dahil. 4 adet " + TL(h.size.price * 4) + ", söküm, takma, balans ve sibop dahil.</small>";
          cell.appendChild(price);
          if (h.size.skus.length > 1){
            var ul = document.createElement("ul"); ul.className = "skus";
            h.size.skus.forEach(function(k){ var li = document.createElement("li"); li.innerHTML = "<span>" + skuLabel(k) + "</span><span>" + TL(k.price) + "</span>"; ul.appendChild(li); });
            cell.appendChild(ul);
          }
        } else {
          price.className = "price ask"; price.textContent = "Fiyat için WhatsApp'tan sor."; cell.appendChild(price);
        }
        var l2 = document.createElement("a"); l2.className = "tlink"; l2.target = "_blank"; l2.rel = "noopener";
        var ptxt = h.size.price ? " Listede " + TL(h.size.price) + " görünüyor." : "";
        l2.href = waHref("Merhaba, " + disp + " Michelin " + h.family.name + " için stok ve fiyat sormak istiyorum." + ptxt + forVehicle); l2.textContent = "WhatsApp'tan sor";
        cell.appendChild(l2); grid.appendChild(cell);
      });
    }
    priceNote.textContent = priceList ? "Fiyatlar " + priceList.label + " Michelin liste fiyatıdır, KDV dahil, lastik başına. Kampanya ve stok için WhatsApp'tan yazın." : "";
    var hk = "#" + key(sz.w, sz.a, sz.r, sz.c);
    if (location.hash !== hk) history.replaceState(null, "", hk);
  }

  function buildIndex(data){
    families = data.families; priceList = data.priceList || null;
    families.forEach(function(f){
      f.sizes.forEach(function(s){
        var k = s.key;
        (index[k] = index[k] || []).push({ family: f, size: s });
        var c = s.commercial ? 1 : 0;
        tree[c] = tree[c] || {};
        tree[c][s.width] = tree[c][s.width] || {};
        var rims = tree[c][s.width][s.aspect] = tree[c][s.width][s.aspect] || [];
        if (rims.indexOf(s.rim) === -1) rims.push(s.rim);
      });
    });
    var fromHash = parseKey(location.hash.replace(/^#/, ""));
    if (fromHash && index[key(fromHash.w, fromHash.a, fromHash.r, fromHash.c)]) setSize(fromHash.w, fromHash.a, fromHash.r, fromHash.c);
    else setSize(225, 45, 18, false);
    render();
  }

  function fallback(){
    /* Catalog not reachable: keep the finder usable, route to WhatsApp with the chosen size. */
    var ws = [145,155,165,175,185,195,205,215,225,235,245,255,265,275,285,295,305,315,325,335,345,355];
    var as = [25,30,35,40,45,50,55,60,65,70,75,80];
    var rs = [13,14,15,16,17,18,19,20,21,22,23];
    fill(selW, ws, 225); fill(selA, as, 45); fill(selR, rs, 18);
    note.textContent = "Liste şu an yüklenemedi. Ebadı seç, WhatsApp'tan soralım.";
    var btn = document.getElementById("findBtn"); btn.textContent = "Bu ebadı WhatsApp'tan sor";
    form.addEventListener("submit", function(ev){
      ev.preventDefault();
      window.open(waHref("Merhaba, " + display(selW.value, selA.value, selR.value, isC()) + " Michelin lastik fiyatı alabilir miyim?"), "_blank", "noopener");
    });
    title.textContent = "";
  }

  function manual(){ vehicle = null; }
  selW.addEventListener("change", function(){ manual(); fillAspects(); fillRims(); if (families) render(); });
  selA.addEventListener("change", function(){ manual(); fillRims(); if (families) render(); });
  selR.addEventListener("change", function(){ manual(); if (families) render(); });
  cToggle.addEventListener("click", function(){
    manual();
    cToggle.setAttribute("aria-pressed", String(!isC()));
    if (families){ fillWidths(); fillAspects(); fillRims(); render(); }
  });
  function scrollResults(){ document.getElementById("results").scrollIntoView({ behavior: reduced ? "auto" : "smooth", block: "start" }); }
  form.addEventListener("submit", function(ev){
    if (!families) return;
    ev.preventDefault();
    if (!panelVehicle.hidden) return;
    manual(); render(); scrollResults();
  });

  fetch("assets/michelin-catalog.json").then(function(r){ if (!r.ok) throw new Error(r.status); return r.json(); })
    .then(buildIndex).catch(fallback);

  /* Rail: "Ebatları gör" preselects the family's first size */
  document.querySelectorAll("a[data-family]").forEach(function(a){
    a.addEventListener("click", function(){
      var p = parseKey(a.getAttribute("data-size"));
      if (!p || !families) return;
      pendingFamily = a.getAttribute("data-family"); vehicle = null;
      setMode("size"); setSize(p.w, p.a, p.r, p.c); render();
    });
  });

  /* Finder modes */
  var modeSize = document.getElementById("modeSize"), modeVehicle = document.getElementById("modeVehicle");
  var panelSize = document.getElementById("panelSize"), panelVehicle = document.getElementById("panelVehicle");
  function setMode(m){
    var v = m === "vehicle";
    modeSize.setAttribute("aria-selected", String(!v)); modeVehicle.setAttribute("aria-selected", String(v));
    panelSize.hidden = v; panelVehicle.hidden = !v;
    if (v) initVehicle();
  }
  modeSize.addEventListener("click", function(){ setMode("size"); });
  modeVehicle.addEventListener("click", function(){ setMode("vehicle"); });
  document.querySelectorAll('a[data-mode="vehicle"]').forEach(function(a){ a.addEventListener("click", function(){ setMode("vehicle"); }); });

  /* Vehicle mode: make → model → year → version → factory sizes. Data: assets/fitment (autoevolution, 2024-10). */
  var CURRENT_YEAR = Math.min(2025, new Date().getFullYear());
  var LCV = /\b(transit|transporter|caravelle|multivan|crafter|doblo|dobl[oò]|fiorino|scudo|ducato|talento|kangoo|master|trafic|express|partner|expert|boxer|rifter|berlingo|jumpy|jumper|combo|vivaro|movano|caddy|vito|sprinter|hiace|proace|nv200|nv300|nv400|primastar|interstar|h-1|h350|staria|dispatch|relay)\b/i;
  var MISSING = "__missing__";
  var vMake = document.getElementById("vMake"), vModel = document.getElementById("vModel"), vYear = document.getElementById("vYear");
  var vVersion = document.getElementById("vVersion"), vVersionField = document.getElementById("vVersionField"), vResults = document.getElementById("vResults"), vNote = document.getElementById("vNote");
  var fitIndex = null, brandFiles = {}, vInit = false, variants = [];

  function opts(sel, values, placeholder){
    sel.innerHTML = "";
    var o = document.createElement("option"); o.value = ""; o.textContent = placeholder || "Seçin"; sel.appendChild(o);
    values.forEach(function(v){
      var x = document.createElement("option");
      if (typeof v === "object"){ x.value = v.value; x.textContent = v.label; if (v.title) x.title = v.title; }
      else { x.value = v; x.textContent = v; }
      sel.appendChild(x);
    });
    sel.disabled = false;
  }
  function reset(sel, placeholder){ sel.innerHTML = ""; var o = document.createElement("option"); o.value = ""; o.textContent = placeholder || "Seçin"; sel.appendChild(o); sel.disabled = true; }
  function getJson(u){ return fetch(u).then(function(r){ if (!r.ok) throw new Error(r.status); return r.json(); }); }

  function initVehicle(){
    if (vInit) return; vInit = true;
    reset(vMake, "Yükleniyor");
    getJson("assets/fitment/index.json").then(function(d){
      fitIndex = d;
      var makes = d.brands.map(function(b){ return b.brand; });
      makes.push({ value: MISSING, label: "Markam listede yok" });
      opts(vMake, makes);
    }).catch(function(){
      reset(vMake, "Yüklenemedi");
      vResults.innerHTML = "";
      vNote.innerHTML = "Araç verisi yüklenemedi. <a class=\"tlink\" href=\"" + waHref("Merhaba, aracım için Michelin lastik ebadı ve fiyatı öğrenmek istiyorum. Araç: ") + "\" target=\"_blank\" rel=\"noopener\">WhatsApp'tan yaz</a>, biz bulalım.";
    });
  }
  function brandFile(make){
    var e = fitIndex.brands.filter(function(b){ return b.brand === make; })[0];
    if (!e) return Promise.resolve(null);
    if (brandFiles[e.key]) return Promise.resolve(brandFiles[e.key]);
    return getJson("assets/fitment/" + e.key + ".json").then(function(d){ brandFiles[e.key] = d; return d; });
  }
  function modelsFor(make){
    var e = fitIndex.brands.filter(function(b){ return b.brand === make; })[0];
    if (!e) return [];
    var ok = e.models.filter(function(m){ return m.sized && m.to >= 1990; });
    var tr = function(a,b){ return a.localeCompare(b, "tr"); };
    var popular = ok.filter(function(m){ return m.pop !== undefined; }).sort(function(a,b){ return a.pop - b.pop; });
    var current = ok.filter(function(m){ return m.pop === undefined && m.to >= 2020; }).sort(function(a,b){ return tr(a.name, b.name); });
    var older = ok.filter(function(m){ return m.pop === undefined && m.to < 2020; }).sort(function(a,b){ return tr(a.name, b.name); });
    return popular.concat(current, older).map(function(m){ return m.name; });
  }
  function covers(g, y){ return g.from !== null && g.from <= y && y <= (g.to === null ? CURRENT_YEAR : g.to); }
  function yearsFor(m){
    var out = [];
    for (var y = Math.min(m.to, CURRENT_YEAR); y >= m.from; y--){
      if (m.gens.some(function(g){ return covers(g, y); })) out.push(y);
    }
    return out;
  }
  function parseSizeText(t){
    var m = /^(\d{3})\/(\d{2,3})\s*Z?R\s*(\d{2}(?:\.5)?)\s*(C)?\b/i.exec(String(t).trim());
    return m ? { w: +m[1], a: +m[2], r: +m[3], c: !!m[4] } : null;
  }
  function lcvRule(model, sz){
    if (sz.c || !LCV.test(model)) return sz;
    return index[key(sz.w, sz.a, sz.r, true)] ? { w: sz.w, a: sz.a, r: sz.r, c: true } : sz;
  }
  function variantsFor(model, m, year){
    var all = m.gens.filter(function(g){ return covers(g, year); }).concat(m.gens.filter(function(g){ return g.from === null; }));
    var count = {};
    all.forEach(function(g){ count[g.label] = (count[g.label] || 0) + 1; });
    var out = [];
    all.forEach(function(g){
      var open = g.to === null || g.to >= CURRENT_YEAR;
      var yl = g.from === null ? "yıl doğrulanmadı" : open ? g.from + " ve sonrası" : g.from + "-" + g.to;
      var needYears = !g.label || count[g.label] > 1;
      var qual = [g.label, needYears ? yl : ""].filter(Boolean).join(" ");
      g.versions.forEach(function(v){
        var sizes = v.s.map(parseSizeText).filter(Boolean).map(function(sz){ return lcvRule(model, sz); });
        var fit;
        if (sizes.length === 2 && key(sizes[0].w, sizes[0].a, sizes[0].r, sizes[0].c) !== key(sizes[1].w, sizes[1].a, sizes[1].r, sizes[1].c)){
          var st = sizes.slice().sort(function(x,y){ return x.w - y.w; });
          fit = [{ sz: st[0], axle: "Ön" }, { sz: st[1], axle: "Arka" }];
        } else {
          var seen = {}; fit = [];
          sizes.forEach(function(sz){ var k = key(sz.w, sz.a, sz.r, sz.c); if (!seen[k]){ seen[k] = 1; fit.push({ sz: sz, axle: "" }); } });
        }
        out.push({ id: g.label + "|" + g.from + "|" + v.n, name: v.n, label: all.length > 1 && qual ? v.n + ", " + qual : v.n, gen: [g.label, yl].filter(Boolean).join(" "), fit: fit });
      });
    });
    return out;
  }

  function showVariant(v){
    vResults.innerHTML = "";
    if (!v) return;
    var label = [vMake.value, vModel.value, v.name, vYear.value].join(" ");
    if (!v.fit.length){
      var n = document.createElement("div"); n.className = "vnote";
      n.innerHTML = "Bu araç için doğrulanmış lastik ebadı bulunamadı. <a class=\"tlink\" href=\"" + waHref("Merhaba, aracım için Michelin lastik ebadı ve fiyatı öğrenmek istiyorum. Araç: " + label) + "\" target=\"_blank\" rel=\"noopener\">WhatsApp'tan sor</a> veya ölçüyü elle seç.";
      vResults.appendChild(n); return;
    }
    v.fit.forEach(function(f, i){
      var b = document.createElement("button"); b.type = "button"; b.className = "vsize";
      var k = key(f.sz.w, f.sz.a, f.sz.r, f.sz.c);
      b.setAttribute("data-size-key", k);
      var hits = index[k] || [];
      var cheapest = hits.map(function(h){ return h.size.price || 0; }).filter(Boolean).sort(num)[0];
      b.innerHTML = "<b>" + display(f.sz.w, f.sz.a, f.sz.r, f.sz.c) + "</b><span>" + [f.axle, "fabrika ebadı", hits.length ? hits.length + " Michelin serisi" + (cheapest ? ", " + TL(cheapest) + "'den" : "") : "listede yok, sor"].filter(Boolean).join(", ") + "</span>";
      b.addEventListener("click", function(){
        vResults.querySelectorAll(".vsize").forEach(function(x){ x.setAttribute("aria-pressed", "false"); });
        b.setAttribute("aria-pressed", "true");
        vehicle = { label: label, make: vMake.value, model: vModel.value, year: vYear.value };
        if (index[k]) setSize(f.sz.w, f.sz.a, f.sz.r, f.sz.c);
        render(f.sz); scrollResults();
      });
      vResults.appendChild(b);
      if (i === 0 && v.gen){ /* generation note after the list */ }
    });
    if (v.gen){ var g = document.createElement("div"); g.className = "vnote"; g.textContent = v.gen + ". Kaynak: üretici verisi, Ekim 2024. Emin olmak için lastiğin yan yüzüne de bak."; vResults.appendChild(g); }
  }

  vMake.addEventListener("change", function(){
    reset(vModel); reset(vYear); vVersionField.hidden = true; vResults.innerHTML = "";
    if (!vMake.value) return;
    if (vMake.value === MISSING){
      var n = document.createElement("div"); n.className = "vnote";
      n.innerHTML = "Listede olmayan araçlar için <a class=\"tlink\" href=\"" + waHref("Merhaba, aracım için Michelin lastik ebadı ve fiyatı öğrenmek istiyorum. Araç: ") + "\" target=\"_blank\" rel=\"noopener\">WhatsApp'tan yaz</a>, biz bulalım. Ya da lastiğin yanındaki ölçüyü \"Ölçüye göre\" sekmesinden seç.";
      vResults.appendChild(n); return;
    }
    opts(vModel, modelsFor(vMake.value));
  });
  vModel.addEventListener("change", function(){
    reset(vYear); vVersionField.hidden = true; vResults.innerHTML = "";
    if (!vModel.value) return;
    reset(vYear, "Yükleniyor");
    brandFile(vMake.value).then(function(file){
      var m = file && file.models[vModel.value];
      if (!m){ reset(vYear); return; }
      opts(vYear, yearsFor(m));
    }).catch(function(){ reset(vYear, "Yüklenemedi"); });
  });
  vYear.addEventListener("change", function(){
    vVersionField.hidden = true; vResults.innerHTML = ""; variants = [];
    if (!vYear.value) return;
    brandFile(vMake.value).then(function(file){
      var m = file && file.models[vModel.value];
      if (!m) return;
      variants = variantsFor(vModel.value, m, +vYear.value);
      if (variants.length > 1){
        opts(vVersion, variants.map(function(v){ return { value: v.id, label: v.name, title: v.label }; }));
        vVersionField.hidden = false;
      } else {
        showVariant(variants[0]);
      }
    });
  });
  vVersion.addEventListener("change", function(){
    var v = variants.filter(function(x){ return x.id === vVersion.value; })[0];
    showVariant(v || null);
  });

'''
s = s[:js_start] + new_js + s[js_end:]
io.open(p, "w", encoding="utf-8", newline="\n").write(s)
print("patched", len(s))
