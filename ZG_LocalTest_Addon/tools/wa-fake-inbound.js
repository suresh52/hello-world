#!/usr/bin/env node
/* ============================================================================
   tools/wa-fake-inbound.js
   ---------------------------------------------------------------------------
   Sends a FAKE but correctly-signed Meta WhatsApp webhook to your LOCAL
   webhook, so you can test the Customer Messages inbox without migrating the
   number and without Meta being able to reach your laptop.

   USAGE (two terminals, from the repo root):
     Terminal 1:  netlify dev
     Terminal 2:  netlify dev:exec node tools/wa-fake-inbound.js

   `netlify dev:exec` injects WHATSAPP_APP_SECRET from your linked site, so
   the HMAC signature matches what the webhook expects.

   OPTIONS
     --url=<webhook url>   default http://localhost:8888/.netlify/functions/whatsapp-webhook
     --phone=<12 digits>   default 919000000001 (fake test customer)
     --only=text           send just the one text message

   WHAT IT SENDS: one envelope with 6 messages -- text, image, audio,
   document, location, and an invented future type. The old webhook silently
   dropped 5 of these 6. After running, all 6 must appear in 💬 Messages.

   SAFE: it only POSTs to the URL you give it. It sends nothing to Meta and
   messages no real person. The media ids are fake, so "Load" on the photo
   and replying to this fake number are EXPECTED to fail with a clear error.

   CLEAN UP afterwards (Supabase SQL editor):
     delete from public.wa_contacts where phone10 = '9000000001';
   ========================================================================= */

const crypto = require('crypto');

function arg(name, def) {
  const hit = process.argv.find((a) => a.startsWith(`--${name}=`));
  return hit ? hit.slice(name.length + 3) : def;
}

const URL_ = arg('url', 'http://localhost:8888/.netlify/functions/whatsapp-webhook');
const PHONE = arg('phone', '919000000001').replace(/\D/g, '');
const ONLY = arg('only', '');
const SECRET = process.env.WHATSAPP_APP_SECRET;

if (!SECRET) {
  console.error('\n✗ WHATSAPP_APP_SECRET is not set in this terminal.');
  console.error('  Run it through Netlify so your site env is loaded:');
  console.error('    netlify dev:exec node tools/wa-fake-inbound.js\n');
  process.exit(1);
}

const now = Math.floor(Date.now() / 1000);
const stamp = Date.now();
// Unique ids every run -- the webhook dedupes on wa_message_id, so reusing
// ids would make a second run look like "nothing happened".
const id = (n) => `wamid.LOCALTEST.${stamp}.${n}`;

let messages = [
  { id: id(1), from: PHONE, timestamp: String(now), type: 'text',
    text: { body: 'Hi, I need 50 Gift Boxes for our office Diwali event. Can you share pricing?' } },
  { id: id(2), from: PHONE, timestamp: String(now + 1), type: 'image',
    image: { id: 'FAKE_MEDIA_IMAGE', mime_type: 'image/jpeg', sha256: 'fake', caption: 'Our company logo for the boxes' } },
  { id: id(3), from: PHONE, timestamp: String(now + 2), type: 'audio',
    audio: { id: 'FAKE_MEDIA_AUDIO', mime_type: 'audio/ogg; codecs=opus', voice: true } },
  { id: id(4), from: PHONE, timestamp: String(now + 3), type: 'document',
    document: { id: 'FAKE_MEDIA_DOC', mime_type: 'application/pdf', filename: 'PO_Diwali_2026.pdf' } },
  { id: id(5), from: PHONE, timestamp: String(now + 4), type: 'location',
    location: { latitude: 12.9716, longitude: 77.5946, name: 'Our Office', address: 'MG Road, Bangalore' } },
  { id: id(6), from: PHONE, timestamp: String(now + 5), type: 'some_future_type',
    some_future_type: { note: 'a message type this code has never seen' } },
];
if (ONLY === 'text') messages = messages.slice(0, 1);

const payload = {
  object: 'whatsapp_business_account',
  entry: [{
    id: 'LOCAL_TEST_WABA',
    changes: [{
      field: 'messages',
      value: {
        messaging_product: 'whatsapp',
        metadata: { display_phone_number: '910000000000', phone_number_id: 'LOCAL_TEST' },
        contacts: [{ wa_id: PHONE, profile: { name: 'Test Customer' } }],
        messages,
      },
    }],
  }],
};

// Sign EXACTLY the bytes we send -- same HMAC-SHA256 the webhook verifies.
const body = JSON.stringify(payload);
const signature = 'sha256=' + crypto.createHmac('sha256', SECRET).update(body, 'utf8').digest('hex');

(async () => {
  console.log(`\nPOST ${URL_}`);
  console.log(`  from ${PHONE} · ${messages.length} message(s): ${messages.map((m) => m.type).join(', ')}`);
  let res;
  try {
    res = await fetch(URL_, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json', 'X-Hub-Signature-256': signature },
      body,
    });
  } catch (e) {
    console.error(`\n✗ Could not reach ${URL_}: ${e.message}`);
    console.error('  Is `netlify dev` running in the other terminal?\n');
    process.exit(1);
  }
  const text = await res.text();
  console.log(`  -> HTTP ${res.status} ${text}`);

  if (res.status === 200) {
    console.log('\n✓ Webhook accepted it. Now check:');
    console.log('  1. http://localhost:8888/admin.html -> 💬 Messages -> "Test Customer"');
    console.log(`  2. All ${messages.length} messages are in the thread`);
    console.log('  3. Supabase: select msg_type, body from wa_messages where phone10 = \'' + PHONE.slice(-10) + '\';');
    console.log('  4. Nothing new in wa_webhook_failures');
    console.log('\nClean up afterwards:');
    console.log(`  delete from public.wa_contacts where phone10 = '${PHONE.slice(-10)}';\n`);
  } else if (res.status === 401) {
    console.error('\n✗ 401 = signature rejected. The secret in this terminal does not match');
    console.error('  the one the webhook sees. Run via `netlify dev:exec`, not plain `node`.\n');
    process.exitCode = 1;
  } else {
    console.error('\n✗ Unexpected status. Read the `netlify dev` terminal for the error.\n');
    process.exitCode = 1;
  }
})();
