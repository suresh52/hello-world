# TSDR — PROJECT HANDOVER CONTEXT (paste this first in the new chat)

I'm Suresh, sole dev/owner of **The Star Dedication Registry (TSDR)** — an independent,
premium symbolic star-dedication registry (separate product from ZivoGift). This is a
continuation. Read this whole handover, then wait for my `TDSR_Master_v#.txt` (full code
dump, fresh upload) + `TDSR_FileIndex.txt` before writing any code.

---

## 0. HOW I EXPECT YOU TO WORK (non-negotiable)

1. **Read my ACTUAL files before writing code. No guessing/bluffing.**
2. **"Done" means the buyer-visible journey works end-to-end** — NOT "code-complete,"
   NOT "syntax passes," NOT "logic test passes." If I can't click it and see it work on
   the deployed site, it is NOT done. Never report reviewed-only work as tested.
3. Tell me explicitly: **what you actually ran/verified vs. what depends on my live
   services** (Cashfree / R2 / email keys / Supabase).
4. Give **FINISHED drop-in files** at correct repo paths, in **ONE ZIP**, only when I ask.
5. Keep the **CSP / no-inline-styles** rule (`scripts/build_csp.mjs` fails the build on any
   inline `style=`; inline JSON-LD is hashed). Move styles to classes in `css/tsdr.css`.
6. **All shipped files must be pure ASCII + HTML entities** (`&middot; &rarr; &copy;`) and
   `\u` escapes in JS — a previous run shipped mojibake (`Â· â†' Â©`). Never again.
7. Deploy is **GitHub → Netlify (browser UI, Git-connected)**, publish dir = `public/`.
   Files placed at repo ROOT are NOT served — everything user-facing goes in `public/`.

---

## 1. WHAT THIS PRODUCT IS (from my original spec — still binding)

A premium, trustworthy, cinematic symbolic star-dedication registry. The *product is the
whole journey*, not a PDF: discover → choose a real catalogue star → create a symbolic
dedication → register → **cinematic reveal** → explore/locate the star → **download a
premium certificate + star map** → **verify permanently** → revisit → share by privacy level.

**Honesty is core** (must be visible on product page, before payment, FAQs, certificate,
verify page, terms): the star is a **real** HYG-catalogue object; the name is a **symbolic**
dedication; no ownership, no scientific-naming claim, no NASA/IAU/ESA recognition. Prefer
"Dedicate a Star" over "Buy a Star." Never fabricate customer counts, reviews, or partners.

**Stack:** Static HTML/JS frontend + Netlify Functions; Supabase (Postgres + Auth, RLS
forced, source of truth); Cashfree (payments); Cloudflare R2 (private artefacts via SigV4
signed URLs); env-configured transactional email. Star data = HYG DB v4.4 (CC BY-SA 4.0).

---

## 2. COMPETITOR BENCHMARK (researched — this is the bar to match)

Every serious competitor (Star Register, ISR, Star-Naming.com, AstraName, star-naming.in)
delivers the SAME 5 things after purchase. TSDR must match all five:

1. **Personalized certificate** (name, date, dedication, coordinates) — delivered by email
   in minutes.
2. **Star map / chart** showing the star's position.
3. **Coordinates (RA/Dec), constellation, magnitude** shown to the user (not just stored).
4. **Email delivery** — email is BOTH the delivery mechanism AND the later lookup key.
5. **Online registry lookup** by registration number showing name, coordinates,
   constellation, and a viewer — NOT just "active."

Other norms: all reputable ones state plainly it's **symbolic, not IAU/NASA** (TSDR already
does this well — keep it). Lookup by registration number shows the full record + often a
star finder/AR viewer.

**Pricing reference (to replace the placeholder — see §4):** digital-only ~$10–$60
(AstraName $9.95; ISR digital $29.95; Star-Registration $44.90); printed/framed $35–$190.
India sites sell via UPI/cards/netbanking. Current TSDR price of ₹1499 (~$18) is a
reasonable mid digital tier BUT it was hardcoded by the assistant, not chosen by me.

---

## 3. CURRENT STATE — honest ledger (verified in code + my live testing)

### WORKING (confirmed)
- Site live on Netlify (Git-connected), building via `node scripts/build_csp.mjs`.
- UI v2 "observatory-at-night" theme (`css/tsdr.css` + `css/reveal.css`).
- Supabase migrations `0001→0004, 0007→0011` applied; `0005` demo seed (400 stars) loaded
  (real HYG `0006` intentionally NOT used for testing). `0011` = promo codes.
- Netlify env: `SUPABASE_URL`, `SUPABASE_ANON_KEY`, `SUPABASE_SERVICE_ROLE_KEY`.
- `/js/config.js` served dynamically from a Function reading env vars
  (`netlify/functions/public-config.mjs` + `netlify.toml` redirect before the 404 catch-all).
- pgcrypto fix kept: `alter extension pgcrypto set schema public;` (reserve returns a row).
- Dedicate flow reserve → draft → pay-init works; **promo `TESTFREE100` (100%)** skips
  Cashfree and produces a registration number.
- Mobile hamburger menu added (CSP-safe toggle in `tsdr.js` + `tsdr.css`).

### BROKEN / MISSING (the real work — these are the gaps vs. the spec & competitors)
1. **No buyer email captured on the dedicate form** — so no delivery and no lookup key.
   (Biggest product hole.)
2. **Certificate + star map + downloads don't generate** — code exists but is gated behind
   Cloudflare R2 + `TSDR_INTERNAL_SECRET`, never configured → produces nothing end-to-end.
3. **Reveal shows a BLANK screen** then dumps to home — the cinematic shell isn't fed real
   dedication data in the tested path.
4. **Verify only says "active"** — must show star name, RA/Dec, constellation, date,
   certificate identity, viewer link (respecting privacy level).
5. **Second/repeat order → "Payment initialisation failed"** — expected when the promo box
   isn't used and Cashfree keys are absent; needs a graceful, code-side handling (clear
   message + resumable pending dedication), NOT "clear cache and retry."
6. **Price is hardcoded** in `pay-init.mjs` (`PRICE_INR.standard = 1499`) — must be
   admin-editable.

### PENDING LIVE SERVICES (not blockers if we go HTML-cert first)
- Cashfree sandbox keys (`CASHFREE_APP_ID`, `CASHFREE_SECRET_KEY`, `CASHFREE_MODE=sandbox`)
  + webhook `…/.netlify/functions/pay-webhook`.
- Cloudflare R2 + `TSDR_INTERNAL_SECRET` (for PDF artefacts).
- Transactional email provider keys (Resend/MSG91) — CONFIRM which is set on THIS site.

---

## 4. DEFINITION OF "DONE" FOR THE NEXT BUILD (so nothing is faked again)

The next run is "done" only when, on the DEPLOYED site, using the free promo path
(no Cashfree/R2 needed):

- [ ] The dedicate form **captures buyer email (required)** + optional phone.
- [ ] Completing a dedication lands on a **real, populated keepsake/reveal page** showing
      symbolic name, honouree, from, message, date, RA/Dec, constellation, magnitude,
      registration number, and the symbolic-dedication disclosure.
- [ ] A **printable certificate in pure HTML/CSS** (no R2) is viewable + `window.print()`
      ready, with a verification link/QR to the record. (R2 PDF wired later.)
- [ ] **Email delivery** sends the keepsake/verify link to the buyer (if email keys exist;
      if not, say so explicitly and leave a clean fallback).
- [ ] **Verify page** shows the full public-safe record (not just "active") + certificate link.
- [ ] **pay-init** handles Cashfree-absent gracefully and repeat/pending orders resume.
- [ ] **Price** is read from an admin-editable source, not hardcoded.
- [ ] For each item above: I'm told **exactly what was run vs. what depends on live keys**.

Recommended approach: **HTML/CSS certificate + reveal first** (works today, zero new
services), then wire R2 PDFs and Cashfree afterwards. Confirm in-chat before building.

---

## 5. TWO DECISIONS I OWE YOU (answer these when we start)

1. **Certificate:** start with the HTML/CSS printable (works now), R2 PDF later? (Recommend yes.)
2. **Email:** is Resend or MSG91 already env-configured on THIS TSDR site, or still pending?
   (Determines whether email delivery turns on now.)
3. **Explore page:** keep clearly-labelled "Demo" sample cards until real public dedications
   exist, or show an empty "No public dedications yet" state? (My call — note my preference.)

---

## 6. RUN PLAN (each run must produce buyer-visible, verified progress)

- **Run A (keepsake + delivery):** email capture → populated reveal → HTML certificate →
  email link → upgraded verify → graceful pay-init → admin price. (This closes §3 gaps 1–6.)
- **Run B:** R2 PDF certificate + star map generation; downloads via signed URLs.
- **Run C:** cinematic reveal modes (celebration/romance/friendship/memorial/newborn/
  achievement) + interactive star viewer polish; account replay/downloads.
- **Run D:** Cashfree sandbox live, SEO/structured data, accessibility, security hardening,
  full end-to-end test with a written run-vs-reviewed report.

Do NOT generate a ZIP until I ask. Do NOT re-litigate settled state above.
```
