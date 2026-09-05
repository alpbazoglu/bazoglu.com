// V6 verification: pins, scrub, tire fully visible, no overflow, V5 data layer. Run: node lab/check-v6.mjs [url]
import { chromium } from "../../bazoglu-site/node_modules/playwright-core/index.mjs";
import fs from "node:fs";

const url = process.argv[2] || "http://127.0.0.1:5182/";
const out = decodeURIComponent(new URL("./shots/", import.meta.url).pathname).replace(/^\/([A-Za-z]:)/, "$1");
fs.mkdirSync(out, { recursive: true });
const browser = await chromium.launch({ channel: "chrome", args: ["--autoplay-policy=no-user-gesture-required"] });
const fails = [];
const note = (s) => console.log("  " + s);
const tireBox = async (page) => page.$eval("#tireMove", (i) => { const r = i.getBoundingClientRect(); return { l: Math.round(r.left), t: Math.round(r.top), r: Math.round(r.right), b: Math.round(r.bottom), w: Math.round(r.width) }; });

for (const w of [390, 820, 1280, 1600, 1920]) {
  const h = w < 1024 ? 844 : 900;
  const ctx = await browser.newContext({ viewport: { width: w, height: h } });
  const page = await ctx.newPage();
  const errors = [];
  page.on("console", (m) => { if (m.type() === "error") errors.push(m.text()); });
  page.on("pageerror", (e) => errors.push(String(e)));
  page.on("requestfailed", (r) => { const f = (r.failure() || {}).errorText || ""; if (!/ABORTED/.test(f)) errors.push("REQ " + r.url() + " " + f); });
  await page.goto(url, { waitUntil: "networkidle" });
  await page.waitForTimeout(1300);
  console.log(`\n[${w}px]`);
  const sw = await page.evaluate(() => document.documentElement.scrollWidth);
  if (sw > w) { fails.push(`${w}: horizontal overflow ${sw}`); note(`OVERFLOW ${sw}`); } else note(`no overflow`);
  const tb = await tireBox(page);
  note(`tire box l=${tb.l} t=${tb.t} r=${tb.r} b=${tb.b} w=${tb.w} (vw=${w} vh=${h})`);
  if (tb.l < 0 || tb.r > w) fails.push(`${w}: hero tire cropped horizontally ${JSON.stringify(tb)}`);
  if (w >= 1024 && (tb.t < 0 || tb.b > h)) fails.push(`${w}: hero tire cropped vertically ${JSON.stringify(tb)}`);
  const total = await page.evaluate(() => document.documentElement.scrollHeight / window.innerHeight);
  note(`page height = ${total.toFixed(1)} vh`);
  await page.screenshot({ path: `${out}/${w}-00-top.png` });
  if (w >= 1024) {
    // walk the hero pin
    const st = await page.evaluate(() => { const t = ScrollTrigger.getById("hero"); return { s: t.start, e: t.end }; });
    for (const p of [0.25, 0.5, 0.7, 0.86, 1.0]) {
      await page.evaluate((y) => window.scrollTo(0, y), st.s + (st.e - st.s) * p);
      await page.waitForTimeout(350);
      const tb2 = await tireBox(page);
      const rot = await page.$eval("#heroTire", (i) => i.style.transform);
      note(`hero p=${p}: tire l=${tb2.l} r=${tb2.r} t=${tb2.t} b=${tb2.b} ${rot}`);
      if (tb2.l < 0 || tb2.r > w || tb2.t < -2 || tb2.b > h + 2) fails.push(`${w}: tire leaves viewport at hero p=${p} ${JSON.stringify(tb2)}`);
      await page.screenshot({ path: `${out}/${w}-01-hero-${p}.png` });
    }
    const cardIn = await page.$eval("#heroFinder", (c) => { const r = c.getBoundingClientRect(); return r.top >= 0 && r.bottom <= window.innerHeight; });
    if (!cardIn) fails.push(`${w}: finder card not fully inside stage at hero end`);
    // montaj
    const mt = await page.evaluate(() => { const t = ScrollTrigger.getById("montaj"); return { s: t.start, e: t.end }; });
    for (const p of [0.05, 0.2, 0.5, 0.8, 0.95]) {
      await page.evaluate((y) => window.scrollTo(0, y), mt.s + (mt.e - mt.s) * p);
      await page.waitForTimeout(700);
      const v = await page.$eval("#montajVideo", (v) => ({ t: v.currentTime.toFixed(2), d: v.duration, hidden: v.hidden, rs: v.readyState }));
      const caps = await page.$$eval("#capbox .cap", (a) => a.map((c) => (+c.style.opacity).toFixed(2)).join(","));
      const btn = await page.$eval("#capBtn", (b) => b.style.opacity);
      note(`montaj p=${p}: video t=${v.t}/${v.d} rs=${v.rs} hidden=${v.hidden} caps=[${caps}] btn=${btn}`);
      if (p === 0.5 && +v.t < 5) fails.push(`${w}: montaj video did not scrub (t=${v.t})`);
      await page.screenshot({ path: `${out}/${w}-02-montaj-${p}.png` });
    }
    // rail
    const rt = await page.evaluate(() => { const t = ScrollTrigger.getById("rail"); return t ? { s: t.start, e: t.end } : null; });
    if (!rt) note("rail: everything fits, no pin");
    for (const p of rt ? [0.1, 0.6, 1.0] : []) {
      await page.evaluate((y) => window.scrollTo(0, y), rt.s + (rt.e - rt.s) * p);
      await page.waitForTimeout(700);
      const x = await page.$eval("#rail-yaz", (r) => r.style.transform);
      note(`rail p=${p}: ${x}`);
      await page.screenshot({ path: `${out}/${w}-03-rail-${p}.png` });
    }
    const railEnd = await page.$eval("#rail-yaz", (r) => { const last = r.lastElementChild.getBoundingClientRect(); return { right: Math.round(last.right) }; });
    if (rt && railEnd.right > w + 4) fails.push(`${w}: rail end item still off screen (${railEnd.right})`);
    // tab switch inside rail
    await page.click("#tab-lcv"); await page.waitForTimeout(400);
    const vis = await page.$$eval(".rail-panel:not([hidden]) h3", (a) => a.map((x) => x.textContent));
    if (!vis.includes("Agilis 3")) fails.push(`${w}: tab switch failed`);
    await page.screenshot({ path: `${out}/${w}-03-rail-lcv.png` });
  }
  for (const id of ["olcu", "lastikler", "hizmetler", "subeler", "randevu", "sss"]) {
    await page.evaluate((id) => document.getElementById(id).scrollIntoView(), id);
    await page.waitForTimeout(900);
    await page.screenshot({ path: `${out}/${w}-04-${id}.png` });
  }
  await page.evaluate(() => window.scrollTo(0, document.body.scrollHeight)); await page.waitForTimeout(600);
  await page.screenshot({ path: `${out}/${w}-05-end.png` });
  // loops playing? (scroll a strip into view first)
  await page.evaluate(() => document.querySelector(".strip").scrollIntoView({ block: "center" })); await page.waitForTimeout(1500);
  const loops = await page.$$eval("video[data-loop]", (vs) => vs.map((v) => ({ src: !!v.getAttribute("src"), paused: v.paused })));
  note(`loops: ${JSON.stringify(loops)}`);
  if (w >= 720 && !loops.some((l) => l.src && !l.paused)) fails.push(`${w}: no background loop playing while a strip is in view`);
  if (errors.length) { fails.push(`${w}: errors ${errors.join(" | ")}`); note("ERRORS " + errors.join(" | ")); }
  await ctx.close();
}

// V5 data layer at 1280 (finder inside hero card)
{
  const ctx = await browser.newContext({ viewport: { width: 1280, height: 900 } });
  const page = await ctx.newPage();
  const errors = [];
  page.on("pageerror", (e) => errors.push(String(e)));
  await page.goto(url, { waitUntil: "networkidle" });
  await page.waitForTimeout(800);
  console.log("\n[data layer]");
  const names = await page.$$eval("#resultsGrid .cell h3", (a) => a.map((x) => x.textContent));
  note(`default results: ${names.slice(0, 4).join(", ")}`);
  if (!names.includes("Pilot Sport 5")) fails.push("default results missing PS5");
  await page.click("#cToggle"); await page.selectOption("#selW", "205"); await page.selectOption("#selA", "65"); await page.selectOption("#selR", "16");
  const t = await page.locator("#resultsTitle").textContent();
  note(`C: ${t} hash=${await page.evaluate(() => location.hash)}`);
  if (!/R16C/.test(t)) fails.push("C toggle failed");
  const ps = await page.$$eval("#resultsGrid .cell .price", (a) => a.map((x) => x.textContent.slice(0, 30)));
  note(`prices: ${ps.slice(0, 2).join(" | ")}`);
  if (!ps.some((p) => /TL/.test(p))) fails.push("prices missing");
  // goto-finder click scrolls to hero card position
  await page.evaluate(() => window.scrollTo(0, 0)); await page.waitForTimeout(200);
  await page.click(".nav a[data-goto-finder]"); await page.waitForTimeout(1200);
  const cardVisible = await page.$eval("#heroFinder", (c) => { const r = c.getBoundingClientRect(); return r.top >= 0 && r.bottom <= window.innerHeight; });
  note(`goto finder -> card visible=${cardVisible} scrollY=${await page.evaluate(() => window.scrollY)}`);
  if (!cardVisible) fails.push("goto-finder did not land on the card");
  await page.screenshot({ path: `${out}/1280-06-goto-finder.png` });
  // vehicle mode
  await page.click("#modeVehicle");
  await page.waitForFunction(() => document.querySelectorAll("#vMake option").length > 5);
  await page.selectOption("#vMake", "Fiat"); await page.selectOption("#vModel", "Egea");
  await page.waitForFunction(() => document.querySelectorAll("#vYear option").length > 1);
  const years = await page.$$eval("#vYear option", (o) => o.map((x) => x.value).filter(Boolean));
  await page.selectOption("#vYear", years[0]);
  await page.waitForFunction(() => !document.getElementById("vVersionField").hidden || document.querySelectorAll("#vResults .vsize").length > 0, null, { timeout: 8000 });
  if (await page.$eval("#vVersionField", (f) => !f.hidden)) { const vs = await page.$$eval("#vVersion option", (o) => o.map((x) => x.value).filter(Boolean)); await page.selectOption("#vVersion", vs[0]); }
  await page.waitForSelector("#vResults .vsize");
  await page.screenshot({ path: `${out}/1280-07-vehicle.png` });
  await page.click("#vResults .vsize"); await page.waitForTimeout(900);
  const subT = await page.locator("#resultsSub").textContent();
  note(`vehicle pick: ${subT}`);
  if (!/Fiat Egea/.test(subT)) fails.push("vehicle pick failed");
  await page.screenshot({ path: `${out}/1280-08-after-vehicle.png` });
  if (errors.length) fails.push("data layer errors: " + errors.join(" | "));
  await ctx.close();
}

// reduced motion
{
  const ctx = await browser.newContext({ viewport: { width: 1280, height: 900 }, reducedMotion: "reduce" });
  const page = await ctx.newPage();
  await page.goto(url, { waitUntil: "networkidle" });
  await page.evaluate(() => window.scrollTo(0, 900)); await page.waitForTimeout(400);
  const tr = await page.$eval("#heroTire", (i) => i.style.transform);
  const pins = await page.evaluate(() => ScrollTrigger.getAll().length);
  const capOp = await page.$eval("#capbox .cap", (c) => getComputedStyle(c).opacity);
  console.log(`\n[reduced] tire transform="${tr}" triggers=${pins} cap opacity=${capOp}`);
  if (tr) fails.push("tire moves under reduced motion");
  if (pins) fails.push("ScrollTriggers active under reduced motion");
  if (capOp !== "1") fails.push("captions hidden under reduced motion");
  await page.evaluate(() => document.getElementById("montaj").scrollIntoView()); await page.waitForTimeout(400);
  await page.screenshot({ path: `${out}/1280-09-reduced-montaj.png` });
  await ctx.close();
}

await browser.close();
console.log("\n" + (fails.length ? "FAIL\n- " + fails.join("\n- ") : "All checks passed"));
process.exitCode = fails.length ? 1 : 0;
