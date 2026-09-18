# How to send an event

Use this when you have a device key and want to confirm the pipeline works.

1. Post the event:

   ```bash
   curl -X POST https://in.beacon.example.com/v3/events \
     -H "X-Device-Key: $KEY" -d '{"type":"boot"}'
   ```

2. Check it arrived: `beacon tail --device <id>`.

If you are on a private collector, replace the host with your collector's
address; the device key is scoped per collector and will not work across them.
