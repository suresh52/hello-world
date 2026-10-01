-- ============================================================================
-- ZIVOGIFT - SEED PERSONALISED FRAMES (launch fix)
-- 20260926_seed_frames.sql
-- ----------------------------------------------------------------------------
-- WHY: `select ... from public.products where type = 'frame'` returned 0 rows
-- on the live database. The storefront (frames.html / js/frames.js) shows all
-- five frames from its hardcoded CONFIG fallback, so customers can add them to
-- the cart -- but create-cashfree-order.js re-reads prices from `products` and
-- rejects the order with "Unknown or inactive product: frame_wordart".
-- Every frame purchase therefore fails at payment.
--
-- This file merges schema-portrait-frames.sql + schema-portrait-frames-v2.sql
-- + schema-frames-pricing.sql into ONE run, in the correct order, with the
-- ASCII size labels ("A4 (8x12 in)", not the Unicode x) that js/frames.js
-- matches on. Shown price will therefore equal charged price.
--
-- SAFE: touches ONLY the five frame_* rows. Uses `on conflict do nothing` for
-- inserts, so it cannot alter your admin-edited prices on notes, add-ons or
-- digital products. Idempotent - re-running converges to the same state.
-- ============================================================================

begin;

-- 1. Column required by the option-delta pricing engine.
alter table public.products
  add column if not exists option_pricing jsonb;

comment on column public.products.option_pricing is
  'Optional per-option price deltas (rupees to add per unit), keyed by option label then value. NULL = no deltas.';

-- 2. Seed the five frame products.
--    Size labels are PLAIN ASCII to byte-match js/frames.js.
insert into public.products
  (id, type, name, description, emoji, price, compare_at_price, options, option_pricing, sort_order, active)
values
(
  'frame_wordart', 'frame', 'Memory Word Portrait',
  'A framed portrait drawn entirely from your own words - every strand made of the messages that matter. Choose 100% Handmade (hand-drawn) or a Digital rendition, from one photo. Matte-laminated, ready to gift.',
  '🖼️', 799, 1999,
  '[{"label":"Creation Type","values":["Handmade","Digital"]},{"label":"Frame Size","values":["A4 (8x12 in)","A3 (12x16 in)"]},{"label":"Language","values":["English","Hindi","Kannada"]}]'::jsonb,
  '{"Creation Type":{"Handmade":700,"Digital":0},"Frame Size":{"A4 (8x12 in)":0,"A3 (12x16 in)":400}}'::jsonb,
  110, true
),
(
  'frame_landsat', 'frame', 'Name Across Earth',
  'Their name spelled from real satellite landscapes - rivers, coastlines and mountains that naturally form each letter - paired with your personal dedication and delivered as a premium framed keepsake.',
  '🛰️', 899, 1799,
  '[{"label":"Frame Size","values":["A4 (8x12 in)","A3 (12x16 in)"]}]'::jsonb,
  '{"Frame Size":{"A4 (8x12 in)":0,"A3 (12x16 in)":400}}'::jsonb,
  120, true
),
(
  'frame_leaf', 'frame', 'Leaf Art Portrait',
  'Their photo, delicately etched onto a real natural leaf and framed. Choose 100% Handmade (hand-etched by an artist) or a Digital rendition printed on a preserved leaf.',
  '🍃', 1299, 2999,
  '[{"label":"Creation Type","values":["Handmade","Digital"]},{"label":"Frame Size","values":["A5 (6x8 in)","A4 (8x12 in)"]}]'::jsonb,
  '{"Creation Type":{"Handmade":900,"Digital":0},"Frame Size":{"A5 (6x8 in)":0,"A4 (8x12 in)":300}}'::jsonb,
  130, true
),
(
  'frame_bornday', 'frame', 'On The Day You Were Born',
  'A beautifully framed poster of the good things the world remembers from their day - uplifting events, a milestone, the song everyone was playing - hand-picked positive moments from their exact birth date.',
  '📅', 699, 1499,
  '[{"label":"Frame Size","values":["A4 (8x12 in)","A3 (12x16 in)"]}]'::jsonb,
  '{"Frame Size":{"A4 (8x12 in)":0,"A3 (12x16 in)":400}}'::jsonb,
  140, true
),
(
  'frame_starmap', 'frame', 'Star Map of the Night It Happened',
  'The real night sky over the exact date, time and place that changed everything - with the GPS coordinates and your personal message. Astronomically accurate, composed by hand.',
  '🌌', 1299, 2899,
  '[{"label":"Frame Size","values":["A4 (8x12 in)","A3 (12x16 in)"]}]'::jsonb,
  '{"Frame Size":{"A4 (8x12 in)":0,"A3 (12x16 in)":400}}'::jsonb,
  150, true
)
on conflict (id) do nothing;

-- 3. Repair pass: if partial frame rows already existed from an earlier run,
--    force the option maps + ASCII size labels to the correct final state.
--    Scoped to frame_* ids only - no other product is touched.
update public.products
set option_pricing = '{"Creation Type":{"Handmade":700,"Digital":0},"Frame Size":{"A4 (8x12 in)":0,"A3 (12x16 in)":400}}'::jsonb,
    options        = '[{"label":"Creation Type","values":["Handmade","Digital"]},{"label":"Frame Size","values":["A4 (8x12 in)","A3 (12x16 in)"]},{"label":"Language","values":["English","Hindi","Kannada"]}]'::jsonb
where id = 'frame_wordart';

update public.products
set option_pricing = '{"Creation Type":{"Handmade":900,"Digital":0},"Frame Size":{"A5 (6x8 in)":0,"A4 (8x12 in)":300}}'::jsonb,
    options        = '[{"label":"Creation Type","values":["Handmade","Digital"]},{"label":"Frame Size","values":["A5 (6x8 in)","A4 (8x12 in)"]}]'::jsonb
where id = 'frame_leaf';

update public.products
set option_pricing = '{"Frame Size":{"A4 (8x12 in)":0,"A3 (12x16 in)":400}}'::jsonb,
    options        = '[{"label":"Frame Size","values":["A4 (8x12 in)","A3 (12x16 in)"]}]'::jsonb
where id in ('frame_landsat', 'frame_bornday', 'frame_starmap');

commit;

-- ── VERIFY (run after commit; expect 5 rows, ASCII "8x12" not "8×12") ───────
-- select id, name, price, active, sort_order, options, option_pricing
-- from public.products
-- where type = 'frame'
-- order by sort_order;
