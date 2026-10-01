# TSDR — Handover Context (paste this into the new chat)

Copy this whole file into the first message of the new chat, and **attach
`StarDedicationRegistry_Runs1-4.zip`** (or the specific files you want changed).
This gives the new session everything it needs to continue without re-deriving.

---

## 1. What this project is
**The Star Dedication Registry (TSDR)** — an independent, premium symbolic star‑dedication
registry (separate product from ZivoGift). A real catalogue star + a symbolic name + a permanent,
verifiable registry record, with a certificate, data‑driven star map, cinematic reveal and
interactive viewer. Honesty is core: the star is real, the name is symbolic, no ownership/no
scientific recognition claims.

## 2. Current status (end of Run 4 — feature complete)
- Built across 4 runs. **202 automated tests pass, 0 failing.**
- Quality gates all clean: **CSP** (strict, no `unsafe-inline`), **A11Y 0**, **SEO 0**, **PERF 0**.
- Remaining work before launch = **live‑service validation only** (Supabase/Cashfree/R2), a
  **Lighthouse** run, and a **physical QR scan**. See `docs/PRE-LAUNCH-CHECKLIST.md`.

## 3. Tech stack + key decisions
- **Static frontend** (no framework) + **Netlify Functions** (Node, ESM `.mjs`).
- **Supabase** (Postgres + Auth) is the **source of truth**; RLS enabled+forced; anon reaches data
  only via public‑safe views + `SECURITY DEFINER` RPCs.
- **Cloudflare R2** for artefacts (private; served via SigV4 signed URLs).
- **Cashfree** payments — webhook = `Base64(HMAC‑SHA256(x‑webhook‑timestamp + rawBody,
  CLIENT_SECRET))`; server sets the price; activation is idempotent on `idempotency_key`.
- **Star data:** HYG database v4.4 (**CC BY‑SA 4.0**). Gaia was rejected (non‑commercial). No
  Stellarium embed (GPL/maintainer stance) — the viewer + QR + star map + certificate are all
  **original code**.

## 4. Repo layout (inside the ZIP)
```
public/                 static site + _headers (GENERATED strict CSP)
  index, dedicate, how-it-works, explore, verify, reveal, about, faqs, contact,
  accessibility, 404, account/, admin/, legal/(7 pages), css/, js/, assets/
  js/config.example.js  → copy to js/config.js at deploy (public anon key only)
netlify/functions/      reserve, draft, pay-init, pay-webhook, verify, account, admin,
                        reveal, download, media-upload, generate-certificate,
                        explore-public, expire-reservations, _shared/*
lib/                    qr.mjs, qr_decode.mjs, starmap.mjs, certificate.mjs
scripts/                import_hyg, generate_demo_pool, build_csp, a11y/seo/perf audits,
                        test/ (logic, functions, qr, run3, cert, e2e, artifacts, mock_db)
supabase/migrations/    0001–0010
docs/                   run reports 1–4, architecture, security baseline + checklist,
                        dataset/licensing, integration-testing, certificate-and-media,
                        deployment, operations, admin, support, backups-and-DR,
                        pre-launch checklist, known limitations, manifests, ZivoGift contract
netlify.toml · package.json · .env.example · README · BUILD-SUMMARY.md
```

## 5. Migrations — apply IN THIS ORDER
`0001 → 0002 → 0003 → 0004 → 0007 → 0008 → 0009 → 0010`, then a seed
(`0005` demo for testing, or generate `0006` real HYG via `npm run import:hyg`).

## 6. Environment variables (set in Netlify UI → Site settings → Environment)
`SUPABASE_URL`, `SUPABASE_ANON_KEY`, `SUPABASE_SERVICE_ROLE_KEY`,
`CASHFREE_APP_ID`, `CASHFREE_SECRET_KEY`, `CASHFREE_MODE`,
`R2_ACCOUNT_ID`, `R2_ACCESS_KEY_ID`, `R2_SECRET_ACCESS_KEY`, `R2_BUCKET`,
`EMAIL_PROVIDER`, `EMAIL_API_KEY`, `EMAIL_FROM`,
`TSDR_PUBLIC_BASE_URL`, `TSDR_RESERVATION_MINUTES`,
`TSDR_ADMIN_ALLOWED_EMAILS`, `TSDR_INTERNAL_SECRET`.
Front‑end public config: `public/js/config.js` (copy from `config.example.js`) — anon key +
`TSDR_CF_MODE` only. NEVER put service‑role/secret keys in the browser.

## 7. IMPORTANT — you deploy via the Netlify browser UI. Read this.
There are two Netlify "UI" paths, and they behave very differently:

- **Git‑connected deploy (RECOMMENDED, required for this project):** connect the repo in the
  Netlify UI. Netlify then runs the build command `node scripts/build_csp.mjs` (generates the
  strict‑CSP `_headers`) **and** deploys the `netlify/functions/*`. This is what the app needs —
  the whole thing (reserve/pay/verify/reveal/certificate) depends on the Functions.

- **Drag‑and‑drop deploy (NOT sufficient alone):** if you drag a folder into the Netlify UI, it
  just uploads static files — **the build command does NOT run and Functions are NOT deployed**.
  If you drag only `public/`, you'd get the pages but every dynamic feature would 404.
  - The generated `public/_headers` IS included in the ZIP, so a drag‑drop of `public/` would
    still apply the strict CSP — but with no Functions, forms won't work.

**Bottom line:** use **Git‑connected** deploy (GitHub/GitLab → Netlify) so the build command +
Functions deploy. `netlify.toml` already sets: publish=`public`, functions=`netlify/functions`,
build=`node scripts/build_csp.mjs`. Set the env vars in the UI. Add `public/js/config.js`.

Also: after ANY HTML/CSS change, the CSP `_headers` must be regenerated by the build
(`node scripts/build_csp.mjs`). Git‑connected deploys do this automatically; a raw drag‑drop does
not. If you edit a page and add an inline `style=""`, the build will FAIL on purpose (that's the
CSP guard) — move the style to a class in `public/css/tsdr.css`.

## 8. How to verify locally (optional, before pushing)
```
npm install
npm run verify:all     # audits (csp+a11y+seo+perf) + tests (202)
```
Artifact/cert tests need the doc libs:
`NODE_PATH=/opt/oai-docgen/node_modules npm run test:artifacts` (only relevant in this build
sandbox; on your machine just `npm i pdf-lib sharp` and run with normal Node).

## 9. Gotchas / conventions the new chat must respect
- **Store‑raw / escape‑on‑output:** user text is stored raw (control chars stripped only); every
  HTML sink escapes at output (`textContent`/`esc()`/PDF `safe()`). Do NOT re‑add escaping at
  storage — it double‑encodes (this bug was caught by the e2e test and fixed).
- **No inline styles/scripts** (CSP). Use utility classes in `tsdr.css`; external JS files only;
  inline JSON‑LD is allowed (it's hashed by `build_csp.mjs`).
- **Registration number format:** `TSDR-YYYY-XXXXXXXX` using a 32‑char alphabet with **no I/L/O/U**.
  Test data must respect this (a Run‑3 test failed because seeds used O/I).
- **pdf‑lib fonts are WinAnsi** → certificate text is sanitised to Latin‑1 (curly quotes, em‑dash,
  minus, ellipsis mapped). Non‑Latin scripts are stripped in the PDF only (record keeps Unicode).
  To support Devanagari/CJK on the certificate, embed a Unicode TTF via fontkit.
- **Functions pattern:** each is `export async function core(event, deps)` (testable) + a thin
  `handler` that injects real deps. Keep this so tests can mock DB/Cashfree/R2.
- **QR** is original code, RS‑verified + decoder round‑tripped, but **not phone‑scanned** yet.

## 10. What's verified vs. what still needs LIVE testing
- Verified in build env (mocks/logic/real libs): allocation atomicity, idempotent payment
  activation, signature verify, verify/reveal privacy, R2 SigV4 structure, real PDF+map+QR
  generation, full e2e journey.
- **NOT yet run live:** migrations against a real Supabase, real Cashfree sandbox order+webhook,
  real R2 upload/download, Lighthouse, physical QR scan. Steps: `docs/INTEGRATION-TESTING.md` +
  `docs/PRE-LAUNCH-CHECKLIST.md`.

## 11. How to start the new chat (suggested first message)
> "Continuing TSDR (context attached + ZIP attached). I'm deploying via Netlify's browser UI
> (Git‑connected). I want to change: <LIST YOUR MODIFICATIONS>. Please read the attached files
> before editing, keep the CSP/no‑inline‑styles rule, and re‑run the audits + tests."
>
> Then list the specific modifications (page copy, pricing, new gift types, colours, fields,
> etc.). If a change touches a specific file, attach that file so it's edited from the real source
> — not guessed.

---
_Product: The Star Dedication Registry. Star data: HYG Database (CC BY‑SA 4.0)._
