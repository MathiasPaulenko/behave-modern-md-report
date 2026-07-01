# 📋 Behave Project Example

**Generated:** 2026-07-01 12:46:33

25 step definitions across 3 files · Given 11, Then 9, When 5

---

## Statistics

| Metric         | Value |
| -------------- | ----- |
| Total steps    | 25    |
| Files          | 3     |
| Parameterised  | 10    |
| With docstring | 0     |
| Regex patterns | 0     |

## Steps by Keyword

| Keyword | Count |
| ------- | ----- |
| Given   | 11    |
| Then    | 9     |
| When    | 5     |

## Steps by File

| File               | Count |
| ------------------ | ----- |
| checkout_steps.py  | 10    |
| login_steps.py     | 8     |
| reporting_steps.py | 7     |

---

## Step Definitions

<details>
<summary>🔵 Given: the cart contains {count:d} items — `step_cart_items`</summary>

#### Location

`checkout_steps.py:10`

#### Parameters

- `count:d`

#### Source

```python
def step_cart_items(context, count=1):
    context.cart = {"items": count, "total": count * 50}
```

</details>

<details>
<summary>🔵 Given: the cart contains 1 item — `step_cart_items`</summary>

#### Location

`checkout_steps.py:10`

#### Parameters

- `count`

#### Source

```python
def step_cart_items(context, count=1):
    context.cart = {"items": count, "total": count * 50}
```

</details>

<details>
<summary>🔵 Given: the total is {total:d} — `step_total`</summary>

#### Location

`checkout_steps.py:15`

#### Parameters

- `total:d`

#### Source

```python
def step_total(context, total):
    context.cart["total"] = total
```

</details>

<details>
<summary>🟡 When: the user pays with "{method}" — `step_pay`</summary>

#### Location

`checkout_steps.py:20`

#### Parameters

- `method`

#### Source

```python
def step_pay(context, method):
    time.sleep(0.05)
    context.payment_accepted = method == "credit card"
    context.payment_method = method
```

</details>

<details>
<summary>🟢 Then: the payment is accepted — `step_payment_accepted`</summary>

#### Location

`checkout_steps.py:27`

#### Source

```python
def step_payment_accepted(context):
    assert context.payment_accepted, "Payment was rejected"
```

</details>

<details>
<summary>🟢 Then: the payment is rejected — `step_payment_rejected`</summary>

#### Location

`checkout_steps.py:32`

#### Source

```python
def step_payment_rejected(context):
    assert not context.payment_accepted, "Payment was unexpectedly accepted"
```

</details>

<details>
<summary>🔵 Given: the order is confirmed — `step_order_confirmed`</summary>

#### Location

`checkout_steps.py:37`

#### Source

```python
def step_order_confirmed(context):
    context.order = {"status": "confirmed"}
```

</details>

<details>
<summary>🟡 When: the user selects "{method}" shipping — `step_select_shipping`</summary>

#### Location

`checkout_steps.py:42`

#### Parameters

- `method`

#### Source

```python
def step_select_shipping(context, method):
    time.sleep(0.03)
    context.shipping = method
```

</details>

<details>
<summary>🟢 Then: the shipping cost is {cost:d} — `step_shipping_cost`</summary>

#### Location

`checkout_steps.py:48`

#### Parameters

- `cost:d`

#### Source

```python
def step_shipping_cost(context, cost):
    expected = {"express": 15, "standard": 5}[context.shipping]
    assert expected == cost, f"Expected shipping cost {cost}, got {expected}"
```

</details>

<details>
<summary>🟢 Then: the order is confirmed — `step_check_confirmed`</summary>

#### Location

`checkout_steps.py:54`

#### Source

```python
def step_check_confirmed(context):
    assert context.order["status"] == "confirmed"
```

</details>

<details>
<summary>🔵 Given: the database is reset — `step_reset_db`</summary>

#### Location

`login_steps.py:7`

#### Source

```python
def step_reset_db(context):
    context.database = {"users": {"alice": "secret1", "bob": "secret2", "locked": "secret"}}
```

</details>

<details>
<summary>🔵 Given: a registered user exists — `step_user_exists`</summary>

#### Location

`login_steps.py:12`

#### Source

```python
def step_user_exists(context):
    assert context.database is not None
```

</details>

<details>
<summary>🔵 Given: the username is "{username}" — `step_set_username`</summary>

#### Location

`login_steps.py:17`

#### Parameters

- `username`

#### Source

```python
def step_set_username(context, username):
    context.username = username
```

</details>

<details>
<summary>🔵 Given: the password is "{password}" — `step_set_password`</summary>

#### Location

`login_steps.py:22`

#### Parameters

- `password`

#### Source

```python
def step_set_password(context, password):
    context.password = password
```

</details>

<details>
<summary>🟡 When: the user logs in — `step_login`</summary>

#### Location

`login_steps.py:27`

#### Source

```python
def step_login(context):
    expected = context.database["users"].get(context.username)
    context.logged_in = expected is not None and expected == context.password
```

</details>

<details>
<summary>🟢 Then: the dashboard is shown — `step_dashboard`</summary>

#### Location

`login_steps.py:33`

#### Source

```python
def step_dashboard(context):
    assert context.logged_in, "User is not logged in"
```

</details>

<details>
<summary>🟢 Then: an error is shown — `step_error`</summary>

#### Location

`login_steps.py:38`

#### Source

```python
def step_error(context):
    assert not context.logged_in, "User unexpectedly logged in"
```

</details>

<details>
<summary>🟢 Then: the account locked message is shown — `step_locked`</summary>

#### Location

`login_steps.py:43`

#### Source

```python
def step_locked(context):
    context.scenario.skip("Account locking logic is not implemented yet")
```

</details>

<details>
<summary>🔵 Given: the report engine is ready — `step_engine_ready`</summary>

#### Location

`reporting_steps.py:9`

#### Source

```python
def step_engine_ready(context):
    context.report = {"rows": 0, "size": 0}
```

</details>

<details>
<summary>🟡 When: the report is generated with {rows:d} rows — `step_generate_report`</summary>

#### Location

`reporting_steps.py:14`

#### Parameters

- `rows:d`

#### Source

```python
def step_generate_report(context, rows):
    time.sleep(0.2)
    context.report["rows"] = rows
    context.report["size"] = rows * 1024
```

</details>

<details>
<summary>🟢 Then: the report is available — `step_report_available`</summary>

#### Location

`reporting_steps.py:21`

#### Source

```python
def step_report_available(context):
    report = getattr(context, "report", {})
    assert report.get("rows", 0) > 0
```

</details>

<details>
<summary>🟢 Then: the report size is greater than {size:d} MB — `step_report_size`</summary>

#### Location

`reporting_steps.py:27`

#### Parameters

- `size:d`

#### Source

```python
def step_report_size(context, size):
    mb = context.report["size"] / (1024 * 1024)
    assert mb > size, f"Report size {mb:.2f} MB is not greater than {size} MB"
```

</details>

<details>
<summary>🔵 Given: the legacy engine is enabled — `step_legacy_engine`</summary>

#### Location

`reporting_steps.py:33`

#### Source

```python
def step_legacy_engine(context):
    pass
```

</details>

<details>
<summary>🔵 Given: the legacy report engine is being implemented — `step_legacy_pending`</summary>

#### Location

`reporting_steps.py:38`

#### Source

```python
def step_legacy_pending(context):
    context.scenario.skip("Legacy report engine not implemented yet")
```

</details>

<details>
<summary>🟡 When: the legacy report is generated — `step_legacy_report`</summary>

#### Location

`reporting_steps.py:43`

#### Source

```python
def step_legacy_report(context):
    pass
```

</details>

---

*Generated by Behave Markdown Report on 2026-07-01 12:46:33.*
