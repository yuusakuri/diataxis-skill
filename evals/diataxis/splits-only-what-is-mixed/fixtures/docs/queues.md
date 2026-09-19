# Queues

We moved to a pull-based queue because the push model made backpressure
invisible: a slow consumer looked healthy right up to the point where the
broker started dropping messages. Pull lets a consumer take work at its own
rate, and the depth metric then means something. We looked at adding a sidecar
to the push model instead and rejected it, because it put the failure in a
process nobody owned.

To create a queue:

1. `qctl create orders --partitions 4`
2. `qctl grant orders --consumer billing`
3. Confirm with `qctl describe orders`

| Setting | Type | Default | Description |
|---|---|---|---|
| `visibility_timeout` | duration | `30s` | How long a taken message is hidden |
| `max_receives` | int | `5` | Deliveries before a message goes to the DLQ |
| `retention` | duration | `4d` | How long an unconsumed message is kept |

In this guide you will build your first consumer. We will start from an empty
project, take a message, acknowledge it, and watch the queue depth drop. By the
end you will have a consumer you wrote yourself running against a real queue.
