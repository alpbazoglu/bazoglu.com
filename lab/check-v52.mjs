import { chromium } from "../../bazoglu-site/node_modules/playwright-core/index.mjs";
const url = process.argv[2] || "http://127.0.0.1:5181/";
const b = await chromium.launch({ channel: "chrome" });
const fails = [];
{
  const p = await (await b.newContext({ viewport: { width: 1280, height: 900 } })).newPage();
  const errs = []; p.on("pageerror", e => errs.push(String(e))); p.on("console", m => { if (m.type() === "error") errs.push(m.text()); });
  await p.goto(url, { waitUntil: "networkidle" }); await p.waitForTimeout(1200);
  const h1 = await p.$eval("h1.words", h => ({ in: h.classList.contains("is-in"), words: h.querySelectorAll(".ws").length, op: getComputedStyle(h.querySelector(".ws:last-child")).opacity, text: h.textContent }));
  console.log("h1", h1); if (!h1.in || h1.op !== "1" || h1.words !== 3) fails.push("h1 words stagger");
  await p.screenshot({ path: "lab/shots/v52-hero.png" });
  await p.evaluate(() => { document.documentElement.style.scrollBehavior = "auto"; document.getElementById("lastikler").scrollIntoView(); });
  await p.waitForTimeout(800);
  const ind = await p.$eval(".tabs", t => { const i = t.querySelector(".ind").getBoundingClientRect(), a = t.querySelector('[aria-selected="true"]').getBoundingClientRect(); return { il: Math.round(i.left), al: Math.round(a.left), iw: Math.round(i.width), aw: Math.round(a.width) }; });
  console.log("tab indicator", ind); if (Math.abs(ind.il - ind.al) > 2 || Math.abs(ind.iw - ind.aw) > 2) fails.push("tab indicator misplaced");
  await p.click("#tab-kis"); await p.waitForTimeout(500);
  const ind2 = await p.$eval(".tabs", t => { const i = t.querySelector(".ind").getBoundingClientRect(), a = t.querySelector('[aria-selected="true"]').getBoundingClientRect(); return Math.abs(i.left - a.left) < 2 && Math.abs(i.width - a.width) < 2; });
  if (!ind2) fails.push("tab indicator did not move");
  await p.screenshot({ path: "lab/shots/v52-tabs.png" });
  const sb = await p.$eval("#scrollbar", s => s.style.transform); console.log("scrollbar", sb); if (!/scaleX\(0\.\d/.test(sb)) fails.push("scroll progress not updating");
  // prices count-up final value
  await p.evaluate(() => document.getElementById("results").scrollIntoView()); await p.waitForTimeout(1400);
  const price = await p.$eval("#resultsGrid .cell .price b", b => b.textContent); console.log("price after countup:", price); if (!/^\d{1,3}(\.\d{3})* TL$/.test(price) || price === "0 TL") fails.push("count-up final wrong: " + price);
  await p.screenshot({ path: "lab/shots/v52-prices.png" });
  // FAQ
  await p.evaluate(() => document.getElementById("sss").scrollIntoView()); await p.waitForTimeout(600);
  await p.click(".faq details:nth-child(2) summary"); await p.waitForTimeout(600);
  const faq = await p.$eval(".faq details:nth-child(2)", d => ({ open: d.open, h: d.querySelector(".a").getBoundingClientRect().height }));
  console.log("faq", faq); if (!faq.open || faq.h < 20) fails.push("faq did not open");
  await p.screenshot({ path: "lab/shots/v52-faq.png" });
  await p.click(".faq details:nth-child(2) summary"); await p.waitForTimeout(600);
  const closed = await p.$eval(".faq details:nth-child(2)", d => !d.open); if (!closed) fails.push("faq did not close");
  // modes indicator
  await p.evaluate(() => document.getElementById("olcu").scrollIntoView()); await p.click("#modeVehicle"); await p.waitForTimeout(500);
  const mind = await p.$eval(".modes", t => { const i = t.querySelector(".ind").getBoundingClientRect(), a = t.querySelector('[aria-selected="true"]').getBoundingClientRect(); return Math.abs(i.left - a.left) < 2 && Math.abs(i.width - a.width) < 2; });
  if (!mind) fails.push("modes indicator misplaced");
  // magnetic
  const btn = await p.$(".hero .btn-yellow"); await p.evaluate(() => window.scrollTo(0, 0)); await p.waitForTimeout(300);
  const box = await btn.boundingBox(); await p.mouse.move(box.x + box.width * 0.9, box.y + box.height * 0.8); await p.waitForTimeout(200);
  const tr = await btn.evaluate(b => b.style.transform); console.log("magnetic", tr); if (!/translate\(/.test(tr)) fails.push("magnetic no effect");
  if (errs.length) fails.push("console: " + errs.join(" | "));
  await p.context().close();
}
{
  const p = await (await b.newContext({ viewport: { width: 390, height: 844 } })).newPage();
  await p.goto(url, { waitUntil: "networkidle" });
  const fab0 = await p.$eval("#fab", f => f.classList.contains("is-on"));
  await p.evaluate(() => { document.documentElement.style.scrollBehavior = "auto"; window.scrollTo(0, 1200); }); await p.waitForTimeout(500);
  const fab1 = await p.$eval("#fab", f => ({ on: f.classList.contains("is-on"), disp: getComputedStyle(f).display, op: getComputedStyle(f).opacity }));
  console.log("fab", fab0, fab1); if (fab0 || !fab1.on || fab1.disp !== "flex" || fab1.op !== "1") fails.push("fab state wrong");
  const sw = await p.evaluate(() => document.documentElement.scrollWidth); if (sw > 390) fails.push("mobile overflow " + sw);
  await p.screenshot({ path: "lab/shots/v52-mobile.png" });
  await p.evaluate(() => document.getElementById("sss").scrollIntoView()); await p.waitForTimeout(500);
  await p.screenshot({ path: "lab/shots/v52-mobile-faq.png" });
  await p.context().close();
}
await b.close();
console.log(fails.length ? "FAIL\n- " + fails.join("\n- ") : "v5.2 checks passed");
process.exitCode = fails.length ? 1 : 0;
