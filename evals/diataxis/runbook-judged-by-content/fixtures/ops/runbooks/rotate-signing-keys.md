# Rotate the JWT signing keys

Do this every 90 days, and immediately if a key may have been exposed.

1. Generate the new key pair:

   ```bash
   authctl keys generate --alg RS256 --label $(date +%Y%m)
   ```

2. Publish the public key to the JWKS endpoint:

   ```bash
   authctl keys publish <key-id>
   ```

3. Wait for the JWKS cache TTL (10 minutes) so verifiers pick it up.
4. Promote the new key to signing:

   ```bash
   authctl keys promote <key-id>
   ```

5. Retire the old key after the longest token lifetime has passed (24 hours).

If you run the self-hosted auth service, step 3 is not automatic: restart the
verifier pods so they refetch the JWKS document.

If tokens start failing verification between steps 4 and 5, the old key was
retired too early. Re-publish it with `authctl keys publish <old-key-id>` and
wait out the token lifetime again.
