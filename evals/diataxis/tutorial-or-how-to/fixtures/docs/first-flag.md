# Your first feature flag

We will create a feature flag, wire it into a request handler, and watch it
switch a response on and off.

Before you start you need an account on the dashboard, the `flagctl` CLI on your
PATH, and a checkout of the `example-shop` repository. If you already run
flags in production, you can still work through this — nothing here touches a
live project.

## 1. Create the flag

```bash
flagctl create checkout-banner --project example-shop
```

You should see:

```
created flag checkout-banner (off)
```

## 2. Read the flag in the handler

Add this to `handlers/checkout.py`:

```python
if flags.enabled("checkout-banner"):
    return render("checkout_with_banner.html")
```

Restart the server. The page still looks the same, because the flag is off.

## 3. Turn the flag on

```bash
flagctl set checkout-banner --on
```

Reload the checkout page. The banner is there.

## What we did

We created a flag, read it from application code, and flipped it. The banner
appeared without a deploy, which is the whole point of a flag.
