import { chromium } from "../../bazoglu-site/node_modules/playwright-core/index.mjs";
const b = await chromium.launch({ channel: "chrome" });
for (const w of [1280, 390]) {
  const p = await (await b.newContext({ viewport: { width: w, height: 900 } })).newPage();
  await p.goto("http://127.0.0.1:5181/", { waitUntil: "networkidle" });
  await p.click("#modeVehicle");
  await p.waitForFunction(() => document.querySelectorAll("#vMake option").length > 5);
  await p.selectOption("#vMake", "Volkswagen"); await p.selectOption("#vModel", "Tiguan");
  await p.waitForFunction(() => document.querySelectorAll("#vYear option").length > 1);
  const ys = await p.$$eval("#vYear option", o => o.map(x => x.value).filter(Boolean)); await p.selectOption("#vYear", ys[0]);
  await p.waitForFunction(() => !document.getElementById("vVersionField").hidden || document.querySelectorAll("#vResults .vsize").length > 0);
  if (await p.$eval("#vVersionField", f => !f.hidden)) { const vs = await p.$$eval("#vVersion option", o => o.map(x => x.value).filter(Boolean)); await p.selectOption("#vVersion", vs[0]); }
  await p.waitForSelector("#vResults .vsize");
  await p.evaluate(() => { document.documentElement.style.scrollBehavior = "auto"; document.querySelector(".finder").scrollIntoView(); window.scrollBy(0, -90); });
  await p.waitForTimeout(500);
  await p.screenshot({ path: `lab/shots/${w}-vehicle-panel.png` });
  console.log(w, await p.$$eval("#vResults .vsize", b => b.map(x => x.textContent)));
}
await b.close();
