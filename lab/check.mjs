// Verification for bazoglu-v5/index.html. Run: node lab/check.mjs [url]
import { chromium } from "../../bazoglu-site/node_modules/playwright-core/index.mjs";
import fs from "node:fs";

const url = process.argv[2] || "http://127.0.0.1:5181/";
const out = decodeURIComponent(new URL("./shots/", import.meta.url).pathname).replace(/^\/([A-Za-z]:)/, "$1");
fs.mkdirSync(out, { recursive: true });
const browser = await chromium.launch({ channel: "chrome" });
const fails = [];
const note = (s) => console.log("  " + s);

for (const w of [360, 390, 820, 1280, 1600]) {
  const ctx = await browser.newContext({ viewport: { width: w, height: 900 } });
  const page = await ctx.newPage();
  const errors = [];
  page.on("console", (m) => { if (m.type() === "error") errors.push(m.text()); });
  page.on("pageerror", (e) => errors.push(String(e)));
  page.on("requestfailed", (r) => errors.push("REQ " + r.url()));
  await page.goto(url, { waitUntil: "networkidle" });
  await page.waitForTimeout(600);
  console.log(`\n[${w}px]`);
  const sw = await page.evaluate(() => document.documentElement.scrollWidth);
  if (sw > w) { fails.push(`${w}: horizontal overflow scrollWidth=${sw}`); note(`OVERFLOW ${sw}`); } else note(`no overflow (${sw})`);
  // h1 lines
  const h1 = await page.evaluate(() => { const h = document.querySelector("h1"); const r = h.getBoundingClientRect(); const lh = parseFloat(getComputedStyle(h).lineHeight); return { lines: Math.round(r.height / lh), w: r.width, right: r.right }; });
  note(`h1 lines=${h1.lines} width=${Math.round(h1.w)} right=${Math.round(h1.right)}`);
  if (h1.right > w) fails.push(`${w}: h1 clipped`);
  // finder results
  const cells = await page.locator("#resultsGrid .cell").count();
  const rt = await page.locator("#resultsTitle").textContent();
  const names = await page.$$eval("#resultsGrid .cell h3", (a) => a.map((x) => x.textContent));
  note(`results: "${rt}" cells=${cells} [${names.slice(0, 4).join(", ")}...]`);
  if (!names.includes("Pilot Sport 5") || !names.includes("Primacy 5")) fails.push(`${w}: default results missing PS5/Primacy 5`);
  if (errors.length) { fails.push(`${w}: console errors ${errors.join(" | ")}`); note("ERRORS " + errors.join(" | ")); }
  await page.screenshot({ path: `${out}/${w}-top.png` });
  await page.screenshot({ path: `${out}/${w}-full.png`, fullPage: true });
  await ctx.close();
}

// Interaction checks at 1280
{
  const ctx = await browser.newContext({ viewport: { width: 1280, height: 900 } });
  const page = await ctx.newPage();
  await page.goto(url, { waitUntil: "networkidle" });
  await page.waitForTimeout(500);
  console.log("\n[interactions]");
  // C toggle → 205/65 R16C
  await page.click("#cToggle");
  await page.selectOption("#selW", "205");
  await page.selectOption("#selA", "65");
  await page.selectOption("#selR", "16");
  const names = await page.$$eval("#resultsGrid .cell h3", (a) => a.map((x) => x.textContent));
  const t = await page.locator("#resultsTitle").textContent();
  note(`C: "${t}" -> ${names.join(", ")}`);
  if (!/R16C/.test(t) || !names.some((n) => /Agilis/.test(n))) fails.push("C toggle 205/65 R16C did not show Agilis");
  const hash = await page.evaluate(() => location.hash);
  note(`hash=${hash}`);
  if (hash !== "#205-65-16C") fails.push("hash not mirrored");
  // wa link encoded
  const wa = await page.$eval("#resultsGrid .cell a.tlink", (a) => a.href);
  note(`wa=${decodeURIComponent(wa)}`);
  if (!/wa\.me\/905331433270\?text=/.test(wa) || !/205%2F65/.test(wa)) fails.push("WA link not encoded with size");
  const heroWa = await page.$eval(".nav .btn-yellow", (a) => a.href);
  if (!/text=Merhaba/.test(heroWa)) fails.push("nav WA not prefilled");
  // hash load
  await page.goto(url + "#195-55-16"); await page.reload({ waitUntil: "networkidle" });
  await page.waitForTimeout(400);
  const t2 = await page.locator("#resultsTitle").textContent();
  note(`hash load: "${t2}"`);
  if (!t2.startsWith("195/55 R16 ")) fails.push("hash preload failed");
  // tire rotation
  await page.evaluate(() => { document.documentElement.style.scrollBehavior = "auto"; window.scrollTo(0, 600); });
  await page.waitForTimeout(300);
  const tr = await page.$eval("#heroTire", (i) => i.style.transform);
  note(`tire transform at 600: ${tr}`);
  if (!/rotate\(72/.test(tr)) fails.push("tire rotation wrong: " + tr);
  // tabs
  await page.click("#tab-lcv");
  const vis = await page.$$eval(".rail-panel:not([hidden]) h3", (a) => a.map((x) => x.textContent));
  note(`LCV tab: ${vis.join(", ")}`);
  if (!vis.includes("Agilis 3")) fails.push("tab switch failed");
  // rail link preselect
  await page.click('#rail-lcv a[data-family="agilis-3"]');
  await page.waitForTimeout(300);
  const t3 = await page.locator("#resultsTitle").textContent();
  const first = await page.$eval("#resultsGrid .cell h3", (h) => h.textContent);
  note(`rail link: "${t3}" first=${first}`);
  if (!/R15C/.test(t3) || first !== "Agilis 3") fails.push("rail 'Ebatları gör' preselect failed");
  // scroll to results screenshot + sections
  for (const id of ["olcu", "lastikler", "hizmetler", "randevu", "subeler"]) {
    await page.evaluate((id) => document.getElementById(id).scrollIntoView(), id);
    await page.waitForTimeout(900);
    await page.screenshot({ path: `${out}/1280-${id}.png` });
  }
  await ctx.close();
}

// reduced motion
{
  const ctx = await browser.newContext({ viewport: { width: 1280, height: 900 }, reducedMotion: "reduce" });
  const page = await ctx.newPage();
  await page.goto(url, { waitUntil: "networkidle" });
  await page.evaluate(() => window.scrollTo(0, 800));
  await page.waitForTimeout(300);
  const tr = await page.$eval("#heroTire", (i) => i.style.transform);
  const op = await page.$eval("#olcu h2", (h) => getComputedStyle(h).opacity);
  console.log(`\n[reduced] tire transform="${tr}" olcu h2 opacity=${op}`);
  if (tr) fails.push("tire rotates under reduced motion");
  if (op !== "1") fails.push("reveal hidden under reduced motion");
  await ctx.close();
}

// mobile menu
{
  const ctx = await browser.newContext({ viewport: { width: 390, height: 844 } });
  const page = await ctx.newPage();
  await page.goto(url, { waitUntil: "networkidle" });
  await page.click(".menu-btn");
  const open = await page.$eval("#overlay", (o) => o.classList.contains("is-open"));
  await page.screenshot({ path: `${out}/390-menu.png` });
  console.log(`\n[menu] open=${open}`);
  if (!open) fails.push("mobile menu did not open");
  await ctx.close();
}


// Prices + vehicle mode (v5.1)
{
  const ctx = await browser.newContext({ viewport: { width: 1280, height: 900 } });
  const page = await ctx.newPage();
  const errors = [];
  page.on("console", (m) => { if (m.type() === "error") errors.push(m.text()); });
  page.on("pageerror", (e) => errors.push(String(e)));
  await page.goto(url, { waitUntil: "networkidle" });
  await page.waitForTimeout(400);
  console.log("\n[prices]");
  const prices = await page.$$eval("#resultsGrid .cell", (cells) => cells.map((c) => ({ n: c.querySelector("h3").textContent, p: (c.querySelector(".price") || {}).textContent || "" })));
  note(prices.slice(0, 4).map((x) => x.n + " => " + x.p.slice(0, 40)).join(" | "));
  const ps5 = prices.find((x) => x.n === "Pilot Sport 5");
  if (!ps5 || !/10\.000 TL/.test(ps5.p)) fails.push("Pilot Sport 5 225/45 R18 price 10.000 TL missing");
  if (!/4 adet 40\.000 TL/.test(ps5?.p || "")) fails.push("4-tire total missing");
  const pn = await page.locator("#priceNote").textContent();
  if (!/Eylül 2026/.test(pn)) fails.push("price note missing");
  const waP = await page.$eval("#resultsGrid .cell a.tlink", (a) => decodeURIComponent(a.href));
  note("wa: " + waP.slice(0, 120));
  if (!/TL/.test(waP)) fails.push("WA text lacks price");

  console.log("\n[vehicle]");
  await page.click("#modeVehicle");
  await page.waitForFunction(() => document.querySelectorAll("#vMake option").length > 5);
  await page.selectOption("#vMake", "Fiat");
  await page.selectOption("#vModel", "Egea");
  await page.waitForFunction(() => document.querySelectorAll("#vYear option").length > 1);
  const years = await page.$$eval("#vYear option", (o) => o.map((x) => x.value).filter(Boolean));
  note("years: " + years.slice(0, 5).join(",") + " ...");
  await page.selectOption("#vYear", years[0]);
  await page.waitForFunction(() => !document.getElementById("vVersionField").hidden || document.querySelectorAll("#vResults .vsize").length > 0, null, { timeout: 8000 });
  const versionShown = await page.$eval("#vVersionField", (f) => !f.hidden);
  if (versionShown) {
    const vs = await page.$$eval("#vVersion option", (o) => o.map((x) => x.value).filter(Boolean));
    note("versions: " + vs.length);
    await page.selectOption("#vVersion", vs[0]);
  }
  await page.waitForSelector("#vResults .vsize", { timeout: 5000 });
  const sizes = await page.$$eval("#vResults .vsize", (b) => b.map((x) => x.getAttribute("data-size-key") + " " + x.textContent));
  note("sizes: " + sizes.join(" | "));
  if (!sizes.length) fails.push("vehicle: no sizes for Fiat Egea");
  await page.click("#vResults .vsize");
  await page.waitForTimeout(400);
  const t = await page.locator("#resultsTitle").textContent();
  const subT = await page.locator("#resultsSub").textContent();
  note(`after pick: "${t}" / "${subT}"`);
  if (!/için Michelin serileri/.test(t) || !/Fiat Egea/.test(subT)) fails.push("vehicle pick did not drive results");
  const waV = await page.$eval("#resultsGrid .cell a.tlink", (a) => decodeURIComponent(a.href));
  if (!/Fiat Egea/.test(waV)) fails.push("WA text lacks vehicle");
  // LCV rule: Ford Transit Custom
  await page.selectOption("#vMake", "Ford");
  await page.selectOption("#vModel", "Transit Custom");
  await page.waitForFunction(() => document.querySelectorAll("#vYear option").length > 1);
  const y2 = await page.$$eval("#vYear option", (o) => o.map((x) => x.value).filter(Boolean));
  await page.selectOption("#vYear", y2[0]);
  await page.waitForFunction(() => !document.getElementById("vVersionField").hidden || document.querySelectorAll("#vResults .vsize, #vResults .vnote").length > 0, null, { timeout: 8000 });
  if (await page.$eval("#vVersionField", (f) => !f.hidden)) { const vs = await page.$$eval("#vVersion option", (o) => o.map((x) => x.value).filter(Boolean)); await page.selectOption("#vVersion", vs[0]); }
  await page.waitForTimeout(300);
  const lcv = await page.$$eval("#vResults .vsize", (b) => b.map((x) => x.getAttribute("data-size-key")));
  note("Transit Custom: " + lcv.join(", "));
  // missing make
  await page.selectOption("#vMake", "__missing__");
  const miss = await page.locator("#vResults .vnote").textContent();
  if (!/WhatsApp/.test(miss)) fails.push("missing-make note absent");
  await page.screenshot({ path: `${out}/1280-vehicle.png` });
  if (errors.length) fails.push("v5.1 console errors: " + errors.join(" | "));
  await ctx.close();
}

await browser.close();
console.log("\n" + (fails.length ? "FAIL\n- " + fails.join("\n- ") : "All checks passed"));
process.exitCode = fails.length ? 1 : 0;
