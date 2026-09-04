# Bazoğlu Lastik, bazoglu.com

Tek dosyalık statik site: `index.html` + `assets/`. Derleme yok. Şartname: `../BAZOGLU_PROMPT_V5.md`.

- Fiyatlar: `scripts/build-prices.mjs` (Michelin fiyat listesi Excel → CSV → `assets/michelin-catalog.json`).
- Araç verisi: `assets/fitment/` (autoevolution, Ekim 2024).
- Denetim: `node lab/check.mjs http://127.0.0.1:5181/` (playwright-core, `../bazoglu-site/node_modules`).

Yayın: GitHub Pages, `main` dalı, kök dizin. Alan adı `CNAME` dosyasında.
