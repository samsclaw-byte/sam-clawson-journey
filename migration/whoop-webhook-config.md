# WHOOP Webhook Configuration

## Active Tunnel
**URL:** https://newcastle-olympics-act-municipality.trycloudflare.com/webhook/whoop
**Status:** ✅ Active
**Server:** V2 (with data storage)
**Created:** 2026-02-11 21:56

## Update WHOOP Dashboard

Go to: https://developer.whoop.com/

1. Select your app: "Sams claw"
2. Go to Webhooks section
3. Set Webhook URL to:
   ```
   https://newcastle-olympics-act-municipality.trycloudflare.com/webhook/whoop
   ```
4. Save changes
5. Test webhook (should receive ping)

## Webhook V2 Features

Captures and stores:
- Recovery events (when you wake up)
- Workout events (when you finish exercising)
- Sleep events (when sleep is detected)
- All saved to daily directories: `~/.openclaw/whoop_data/YYYY-MM-DD/`
- Latest summary: `~/.openclaw/whoop_data/latest_summary.json`

## Next: Database Migration

After webhook is confirmed working:
1. Validate all Notion databases
2. Create Airtable bases
3. Migrate data
4. Update Mission Control to use Airtable
