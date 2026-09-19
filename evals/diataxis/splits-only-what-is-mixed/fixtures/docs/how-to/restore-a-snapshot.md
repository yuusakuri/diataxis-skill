# How to restore a snapshot

Snapshots are taken hourly and kept for 14 days, so the version you want is
almost always still there. This is the procedure for putting one back.

1. List what is available: `dbctl snapshots list --cluster <name>`.
2. Restore into a new cluster, never over the running one:

   ```bash
   dbctl snapshots restore <snapshot-id> --into <new-cluster>
   ```

3. Point the application at the new cluster once `dbctl status` reports
   `healthy`.

If you are on the managed tier, step 2 runs asynchronously and returns a job
id; poll it with `dbctl jobs watch <id>`.

If the snapshot predates a schema migration, run the migrations forward before
switching traffic, or the application will fail on the first write.
