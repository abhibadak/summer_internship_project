import 'dotenv/config';
import twilio from 'twilio';

const client = twilio(
  process.env.TWILIO_ACCOUNT_SID,
  process.env.TWILIO_AUTH_TOKEN
);

async function sendSMS(to, body) {
  try {
    const msg = await client.messages.create({
      from: process.env.TWILIO_FROM_NUMBER,
      to,
      body
    });
    console.log(`✅ Message sent! SID: ${msg.sid}`);
  } catch (error) {
    console.error('❌ Failed:', error.message);
  }
}

// Usage: node sendSms.js +919876543210 "Hello world"
if (process.argv.length < 4) {
  console.log('Usage: node sendSms.js <phone_number> "message"');
  process.exit(1);
}

const [, , to, ...msgParts] = process.argv;
sendSMS(to, msgParts.join(' '));
