# Billing webhooks

| Event | Payload | Sent when |
|---|---|---|
| `charge.authorised` | `charge_id`, `amount`, `currency` | An authorisation succeeds |
| `charge.captured` | `charge_id`, `captured_at` | Funds are captured |
| `charge.refunded` | `charge_id`, `refund_id`, `amount` | A refund is accepted |

Signatures use HMAC-SHA256 over the raw body with the endpoint secret. Retries
run for 24 hours with exponential backoff.
