// Merges Bazoğlu's September 2026 Michelin price list into the catalog the site reads.
//   in : ../../_sources/michelin/pricelist-2026-09.csv   (code, desc, list_kdv, price)  price = rightmost "KDV Dahil" column
//        ../../bazoglu-site/src/data/michelin-catalog.json (families + sizes from July list and michelin.com.tr)
//   out: ../assets/michelin-catalog.json  with sizes[].price (lowest KDV-inclusive price) and sizes[].skus [{spec, price, desc}]
// Sizes present in the September list but not in the catalog are added (source "pricelist-2026-09").
// Run-flat SKUs (marked ZP or EMT — Michelin's two names for the same self-supporting casing) are split
// out of their base family into a sibling family "<id>-zp" named "<Name> ZP", so the shop can sell them
// by the name customers ask for. The sibling reuses the base family's render via `img`.
import { readFileSync, writeFileSync } from "node:fs";
import { resolve, dirname } from "node:path";
import { fileURLToPath } from "node:url";
import { parseRow, keyOf } from "../../bazoglu-site/scripts/parse-row.mjs";

const here = dirname(fileURLToPath(import.meta.url));
const CSV = resolve(here, "../../_sources/michelin/pricelist-2026-09.csv");
const CATALOG = resolve(here, "../../bazoglu-site/src/data/michelin-catalog.json");
const OUT = resolve(here, "../assets/michelin-catalog.json");

function parseCsvLine(line) {
  const out = [];
  let cur = "", q = false;
  for (const ch of line) {
    if (ch === '"') q = !q;
    else if (ch === "," && !q) { out.push(cur); cur = ""; }
    else cur += ch;
  }
  out.push(cur);
  return out;
}

const catalog = JSON.parse(readFileSync(CATALOG, "utf8"));
const byId = new Map(catalog.families.map((f) => [f.id, f]));

// ZP = Zero Pressure, EMT = Extended Mobility Technology. Both are Michelin run-flats; the list uses both.
const RUNFLAT = /\b(ZP|EMT)\b/;
// Insert each ZP family right after its base family so the catalog stays grouped by pattern.
function zpFamilyOf(base) {
  const id = base.id + "-zp";
  if (byId.has(id)) return byId.get(id);
  const fam = {
    id,
    name: base.name + " ZP",
    season: base.season,
    segment: base.segment,
    runflat: true,
    img: base.id,            // no separate ZP render exists; the tread pattern is identical
    image: base.image,
    sources: ["pricelist-2026-09"],
    sizes: [],
  };
  byId.set(id, fam);
  catalog.families.splice(catalog.families.indexOf(base) + 1, 0, fam);
  return fam;
}
const lines = readFileSync(CSV, "utf8").replace(/^﻿/, "").split(/\r?\n/).filter(Boolean).slice(1);

let priced = 0, added = 0, runflat = 0;
const unparsed = [];
const displayOf = (s) => `${s.width}/${s.aspect} R${s.rim}${s.commercial ? "C" : ""}`;

for (const line of lines) {
  const [code, desc, , priceRaw] = parseCsvLine(line);
  const price = Math.round(Number(priceRaw));
  if (!desc || !price) continue;
  const p = parseRow(desc);
  if (p.error) { unparsed.push(p); continue; }
  let fam = byId.get(p.family.id);
  if (!fam) { unparsed.push({ error: "family-not-in-catalog", desc }); continue; }
  if (RUNFLAT.test(desc.toUpperCase())) { fam = zpFamilyOf(fam); runflat++; }
  const k = keyOf(p.size);
  let size = fam.sizes.find((s) => s.key === k);
  if (!size) {
    size = { key: k, display: displayOf(p.size), width: p.size.width, aspect: p.size.aspect, rim: p.size.rim, commercial: p.size.commercial, specs: [] };
    fam.sizes.push(size);
    added++;
  }
  const spec = `${p.size.loadIndex}${p.size.loadIndex2 ? "/" + p.size.loadIndex2 : ""}${p.size.speed}`;
  if (!size.specs.includes(spec)) size.specs.push(spec);
  size.skus = size.skus || [];
  size.skus.push({ code: String(code), spec, price, desc: desc.replace(/\s+/g, " ").trim() });
  priced++;
}

catalog.families = catalog.families.filter((f) => f.sizes.length);

let sizesWithPrice = 0, sizesTotal = 0;
for (const f of catalog.families) {
  f.sizes.sort((a, b) => a.width - b.width || a.aspect - b.aspect || a.rim - b.rim || (a.commercial ? 1 : 0) - (b.commercial ? 1 : 0));
  for (const s of f.sizes) {
    sizesTotal++;
    if (s.skus) {
      s.skus.sort((a, b) => a.price - b.price);
      s.price = s.skus[0].price;
      sizesWithPrice++;
    }
  }
}

catalog.priceList = { label: "Eylül 2026", validFrom: "2026-09-01", currency: "TRY", note: "KDV dahil liste fiyatı, lastik başına." };
catalog._note = (catalog._note || "") + " Prices: Bazoğlu Michelin price list September 2026, rightmost KDV-inclusive column, per tire.";
writeFileSync(OUT, JSON.stringify(catalog));
console.log(`priced SKUs=${priced} run-flat=${runflat} families=${catalog.families.length} sizes added=${added} sizes with price=${sizesWithPrice}/${sizesTotal} unparsed=${unparsed.length}`);
for (const u of unparsed) console.log("  ", u.error, "|", u.desc);
