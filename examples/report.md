# ❌ Behave Markdown Report — Demo

**Company:** Open Source

**Status:** Failed  
**Generated:** 2026-06-29 20:09:10  
**Duration:** 1m 1s

---

## Table of Contents

- [Executive Summary](#executive-summary)
- [Statistics](#statistics)
- [Feature Summary](#feature-summary)
- [Tags](#tags)
- [Failed Scenarios](#failed-scenarios)
- [Slowest Scenarios](#slowest-scenarios)
- [Scenario Details](#scenario-details)
- [Environment](#environment)

---

## Executive Summary

| Status    | Count | Icon |
| --------- | ----- | ---- |
| Passed    | 14    | ✅    |
| Failed    | 7     | ❌    |
| Undefined | 4     | ⚠️   |

## Statistics

| Metric           | Value          |
| ---------------- | -------------- |
| Features         | 5              |
| Scenarios        | 25             |
| Steps            | 108            |
| Pass rate        | 56.00%         |
| Total duration   | 1m 1s          |
| Attachments      | 0              |
| Log lines        | 0              |
| Common exception | AssertionError |

## Feature Summary

| Feature                                   | Status       | Scenarios | Duration |
| ----------------------------------------- | ------------ | --------- | -------- |
| [Authentication](#feature-authentication) | ❌ Failed     | 8         | 20.41s   |
| [Checkout](#feature-checkout)             | ❌ Failed     | 5         | 10.70s   |
| [Settings](#feature-settings)             | ❌ Failed     | 4         | 11.39s   |
| [User Login](#feature-user-login)         | ❌ Failed     | 2         | 800ms    |
| [Reporting](#feature-reporting)           | ⚠️ Undefined | 6         | 17.71s   |

## Tags

| Tag              | Count | Passed | Failed | Duration | Pass rate |
| ---------------- | ----- | ------ | ------ | -------- | --------- |
| `authentication` | 8     | 4      | 3      | 20.41s   | 50.00%    |
| `regression`     | 7     | 4      | 3      | 17.00s   | 57.14%    |
| `nightly`        | 6     | 3      | 2      | 16.59s   | 50.00%    |
| `checkout`       | 5     | 2      | 2      | 10.70s   | 40.00%    |
| `api`            | 5     | 3      | 2      | 15.42s   | 60.00%    |
| `smoke`          | 4     | 1      | 2      | 13.14s   | 25.00%    |
| `wip`            | 4     | 2      | 1      | 7.42s    | 50.00%    |
| `settings`       | 4     | 2      | 1      | 11.39s   | 50.00%    |
| `outline`        | 2     | 1      | 1      | 800ms    | 50.00%    |
| `login`          | 2     | 1      | 1      | 800ms    | 50.00%    |
| `payment`        | 2     | 0      | 1      | 4.33s    | 0.00%     |
| `shipping`       | 2     | 1      | 1      | 4.36s    | 50.00%    |
| `reporting`      | 6     | 5      | 0      | 17.71s   | 83.33%    |
| `ui`             | 3     | 3      | 0      | 9.24s    | 100.00%   |

## Failed Scenarios

| Scenario                                                                                                                | Feature        | Status | Reason         | Location                           |
| ----------------------------------------------------------------------------------------------------------------------- | -------------- | ------ | -------------- | ---------------------------------- |
| [Scenario 1: permissions](#scenario-checkout-scenario-1--permissions)                                                   | Checkout       | ❌      | AssertionError | features/Checkout.feature:4        |
| [Scenario 4: permissions](#scenario-checkout-scenario-4--permissions)                                                   | Checkout       | ❌      | AssertionError | features/Checkout.feature:16       |
| [Outline example: Login with invalid credentials](#scenario-user-login-outline-example--login-with-invalid-credentials) | User Login     | ❌      |                | features/login.feature:20          |
| [Scenario 1: permissions](#scenario-authentication-scenario-1--permissions)                                             | Authentication | ❌      | AssertionError | features/Authentication.feature:4  |
| [Scenario 2: checkout](#scenario-authentication-scenario-2--checkout)                                                   | Authentication | ❌      | AssertionError | features/Authentication.feature:8  |
| [Scenario 4: API contract](#scenario-authentication-scenario-4--api-contract)                                           | Authentication | ❌      | AssertionError | features/Authentication.feature:16 |
| [Scenario 3: API contract](#scenario-settings-scenario-3--api-contract)                                                 | Settings       | ❌      | AssertionError | features/Settings.feature:12       |

<details>
<summary>❌ Scenario 1: permissions (Checkout)</summary>

**Location:** `features/Checkout.feature:4`

**Tags:** `payment`

#### Error

```text
Expected 200 but got 500
```

#### Traceback

```python
Traceback (most recent call last):
  File "features/steps/example.py", line 42, in step_impl
    assert response.status_code == 200
AssertionError: Expected 200 but got 500
```

</details>

<details>
<summary>❌ Scenario 4: permissions (Checkout)</summary>

**Location:** `features/Checkout.feature:16`

**Tags:** `shipping`

#### Error

```text
Expected 200 but got 500
```

#### Traceback

```python
Traceback (most recent call last):
  File "features/steps/example.py", line 42, in step_impl
    assert response.status_code == 200
AssertionError: Expected 200 but got 500
```

</details>

<details>
<summary>❌ Outline example: Login with invalid credentials (User Login)</summary>

**Location:** `features/login.feature:20`

**Tags:** `login` `outline`

</details>

<details>
<summary>❌ Scenario 1: permissions (Authentication)</summary>

**Location:** `features/Authentication.feature:4`

**Tags:** `regression` `nightly` `wip`

#### Error

```text
Expected 200 but got 500
```

#### Traceback

```python
Traceback (most recent call last):
  File "features/steps/example.py", line 42, in step_impl
    assert response.status_code == 200
AssertionError: Expected 200 but got 500
```

</details>

<details>
<summary>❌ Scenario 2: checkout (Authentication)</summary>

**Location:** `features/Authentication.feature:8`

**Tags:** `api` `regression` `smoke`

#### Error

```text
Expected 200 but got 500
```

#### Traceback

```python
Traceback (most recent call last):
  File "features/steps/example.py", line 42, in step_impl
    assert response.status_code == 200
AssertionError: Expected 200 but got 500
```

</details>

<details>
<summary>❌ Scenario 4: API contract (Authentication)</summary>

**Location:** `features/Authentication.feature:16`

**Tags:** `smoke`

#### Error

```text
Expected 200 but got 500
```

#### Traceback

```python
Traceback (most recent call last):
  File "features/steps/example.py", line 42, in step_impl
    assert response.status_code == 200
AssertionError: Expected 200 but got 500
```

</details>

<details>
<summary>❌ Scenario 3: API contract (Settings)</summary>

**Location:** `features/Settings.feature:12`

**Tags:** `nightly` `regression` `api`

#### Error

```text
Expected 200 but got 500
```

#### Traceback

```python
Traceback (most recent call last):
  File "features/steps/example.py", line 42, in step_impl
    assert response.status_code == 200
AssertionError: Expected 200 but got 500
```

</details>

## Slowest Scenarios

| Rank | Scenario                                                                      | Feature        | Duration |
| ---- | ----------------------------------------------------------------------------- | -------------- | -------- |
| 1    | [Scenario 4: API contract](#scenario-authentication-scenario-4--api-contract) | Authentication | 4.63s    |
| 2    | [Scenario 6: checkout](#scenario-authentication-scenario-6--checkout)         | Authentication | 4.56s    |
| 3    | [Scenario 5: permissions](#scenario-reporting-scenario-5--permissions)        | Reporting      | 4.18s    |
| 4    | [Scenario 3: API contract](#scenario-settings-scenario-3--api-contract)       | Settings       | 4.11s    |
| 5    | [Scenario 6: API contract](#scenario-reporting-scenario-6--api-contract)      | Reporting      | 4.00s    |
| 6    | [Scenario 2: API contract](#scenario-settings-scenario-2--api-contract)       | Settings       | 3.63s    |
| 7    | [Scenario 8: login flow](#scenario-authentication-scenario-8--login-flow)     | Authentication | 3.31s    |
| 8    | [Scenario 2: reporting](#scenario-checkout-scenario-2--reporting)             | Checkout       | 3.23s    |
| 9    | [Scenario 3: checkout](#scenario-reporting-scenario-3--checkout)              | Reporting      | 2.98s    |
| 10   | [Scenario 1: permissions](#scenario-reporting-scenario-1--permissions)        | Reporting      | 2.77s    |

## Scenario Details

<details>
<summary>Feature: Checkout</summary>

> Behavior of the checkout subsystem including rules.

Tags: `checkout`

#### [Checkout](#feature-checkout)

<details open>
<summary>❌ Scenario: Scenario 1: permissions</summary>

**Status:** ❌ Failed

**Duration:** 1.10s

**Location:** `features/Checkout.feature:4`

**Tags:** `payment`

##### Steps

✅ **When** the user opens the dashboard — `814ms` (Passed)

<sub>Location: `features/steps/example.py:10`</sub>

❌ **Given** the user opens the dashboard — `41ms` (Failed)

<sub>Location: `features/steps/example.py:11`</sub>

> **AssertionError**  
> Expected 200 but got 500

```python
Traceback (most recent call last):
  File "features/steps/example.py", line 42, in step_impl
    assert response.status_code == 200
AssertionError: Expected 200 but got 500
```

✅ **When** the cart contains 1 items — `243ms` (Passed)

<sub>Location: `features/steps/example.py:12`</sub>

</details>

<details>
<summary>⚠️ Scenario: Scenario 2: reporting</summary>

**Status:** ⚠️ Undefined

**Duration:** 3.23s

**Location:** `features/Checkout.feature:8`

**Tags:** `payment`

##### Steps

⚠️ **Then** the response payload matches the schema — `412ms` (Undefined)

<sub>Location: `features/steps/example.py:10`</sub>

✅ **When** the user opens the dashboard — `459ms` (Passed)

<sub>Location: `features/steps/example.py:11`</sub>

✅ **Then** the user opens the dashboard — `877ms` (Passed)

<sub>Location: `features/steps/example.py:12`</sub>

⏭ **Given** the cart contains 2 items — `355ms` (Skipped)

<sub>Location: `features/steps/example.py:13`</sub>

✅ **When** the user opens the dashboard — `795ms` (Passed)

<sub>Location: `features/steps/example.py:14`</sub>

✅ **Given** the response payload matches the schema — `337ms` (Passed)

<sub>Location: `features/steps/example.py:15`</sub>

</details>

<details>
<summary>✅ Scenario: Scenario 3: permissions</summary>

**Status:** ✅ Passed

**Duration:** 1.63s

**Location:** `features/Checkout.feature:12`

**Tags:** `shipping`

##### Steps

✅ **Then** the cart contains 2 items — `764ms` (Passed)

<sub>Location: `features/steps/example.py:10`</sub>

⏭ **When** the response payload matches the schema — `328ms` (Skipped)

<sub>Location: `features/steps/example.py:11`</sub>

⏭ **When** the user opens the dashboard — `279ms` (Skipped)

<sub>Location: `features/steps/example.py:12`</sub>

✅ **Then** the user opens the dashboard — `257ms` (Passed)

<sub>Location: `features/steps/example.py:13`</sub>

</details>

<details open>
<summary>❌ Scenario: Scenario 4: permissions</summary>

**Status:** ❌ Failed

**Duration:** 2.73s

**Location:** `features/Checkout.feature:16`

**Tags:** `shipping`

##### Steps

❌ **And** they click the buy button — `322ms` (Failed)

<sub>Location: `features/steps/example.py:10`</sub>

> **AssertionError**  
> Expected 200 but got 500

```python
Traceback (most recent call last):
  File "features/steps/example.py", line 42, in step_impl
    assert response.status_code == 200
AssertionError: Expected 200 but got 500
```

✅ **Then** the cart contains 7 items — `482ms` (Passed)

<sub>Location: `features/steps/example.py:11`</sub>

✅ **When** the user opens the dashboard — `908ms` (Passed)

<sub>Location: `features/steps/example.py:12`</sub>

✅ **When** the response payload matches the schema — `718ms` (Passed)

<sub>Location: `features/steps/example.py:13`</sub>

✅ **And** the cart contains 8 items — `305ms` (Passed)

<sub>Location: `features/steps/example.py:14`</sub>

</details>

<details>
<summary>✅ Scenario: Scenario 5: checkout</summary>

**Status:** ✅ Passed

**Duration:** 2.00s

**Location:** `features/Checkout.feature:20`

**Tags:** `regression` `nightly`

##### Steps

✅ **Then** the user opens the dashboard — `356ms` (Passed)

<sub>Location: `features/steps/example.py:10`</sub>

✅ **And** the cart contains 5 items — `916ms` (Passed)

<sub>Location: `features/steps/example.py:11`</sub>

⏭ **Given** the cart contains 5 items — `733ms` (Skipped)

<sub>Location: `features/steps/example.py:12`</sub>

</details>

</details>

<details>
<summary>Feature: User Login</summary>

> Login scenarios with background and outline examples.

Tags: `login`

#### [User Login](#feature-user-login)

<details>
<summary>✅ Scenario: Outline example: Login with valid credentials</summary>

**Status:** ✅ Passed

**Duration:** 400ms

**Location:** `features/login.feature:10`

**Tags:** `login` `outline`

##### Examples

| username | password |
| -------- | -------- |
| alice    | secret1  |
| bob      | secret2  |
| carol    | secret3  |

##### Steps

✅ **Given** the username is "alice" — `100ms` (Passed)

✅ **When** the user logs in — `200ms` (Passed)

✅ **Then** the dashboard is shown — `100ms` (Passed)

</details>

<details open>
<summary>❌ Scenario: Outline example: Login with invalid credentials</summary>

**Status:** ❌ Failed

**Duration:** 400ms

**Location:** `features/login.feature:20`

**Tags:** `login` `outline`

##### Examples

| username | password |
| -------- | -------- |
| eve      | wrong    |
| mallory  | bad      |

##### Steps

✅ **Given** the username is "eve" — `100ms` (Passed)

✅ **When** the user logs in — `200ms` (Passed)

❌ **Then** the error is shown — `100ms` (Failed)

</details>

</details>

<details>
<summary>Feature: Authentication</summary>

> Behavior of the authentication subsystem.

Tags: `authentication`

#### [Authentication](#feature-authentication)

<details open>
<summary>❌ Scenario: Scenario 1: permissions</summary>

**Status:** ❌ Failed

**Duration:** 1.67s

**Location:** `features/Authentication.feature:4`

**Tags:** `regression` `nightly` `wip`

##### Steps

❌ **Given** the API returns 200 — `291ms` (Failed)

<sub>Location: `features/steps/example.py:10`</sub>

> **AssertionError**  
> Expected 200 but got 500

```python
Traceback (most recent call last):
  File "features/steps/example.py", line 42, in step_impl
    assert response.status_code == 200
AssertionError: Expected 200 but got 500
```

✅ **Given** the user opens the dashboard — `1.17s` (Passed)

<sub>Location: `features/steps/example.py:11`</sub>

⏭ **When** the cart contains 8 items — `202ms` (Skipped)

<sub>Location: `features/steps/example.py:12`</sub>

</details>

<details open>
<summary>❌ Scenario: Scenario 2: checkout</summary>

**Status:** ❌ Failed

**Duration:** 2.13s

**Location:** `features/Authentication.feature:8`

**Tags:** `api` `regression` `smoke`

##### Steps

✅ **And** the user opens the dashboard — `301ms` (Passed)

<sub>Location: `features/steps/example.py:10`</sub>

✅ **Then** they click the login button — `708ms` (Passed)

<sub>Location: `features/steps/example.py:11`</sub>

✅ **Given** they click the buy button — `86ms` (Passed)

<sub>Location: `features/steps/example.py:12`</sub>

✅ **Then** they click the login button — `338ms` (Passed)

<sub>Location: `features/steps/example.py:13`</sub>

❌ **When** the cart contains 3 items — `694ms` (Failed)

<sub>Location: `features/steps/example.py:14`</sub>

> **AssertionError**  
> Expected 200 but got 500

```python
Traceback (most recent call last):
  File "features/steps/example.py", line 42, in step_impl
    assert response.status_code == 200
AssertionError: Expected 200 but got 500
```

</details>

<details>
<summary>✅ Scenario: Scenario 3: checkout</summary>

**Status:** ✅ Passed

**Duration:** 1.45s

**Location:** `features/Authentication.feature:12`

##### Steps

✅ **And** the user opens the dashboard — `810ms` (Passed)

<sub>Location: `features/steps/example.py:10`</sub>

✅ **Given** the user opens the dashboard — `302ms` (Passed)

<sub>Location: `features/steps/example.py:11`</sub>

✅ **And** they click the login button — `338ms` (Passed)

<sub>Location: `features/steps/example.py:12`</sub>

</details>

<details open>
<summary>❌ Scenario: Scenario 4: API contract</summary>

**Status:** ❌ Failed

**Duration:** 4.63s

**Location:** `features/Authentication.feature:16`

**Tags:** `smoke`

##### Steps

⏭ **Given** the user opens the dashboard — `1.16s` (Skipped)

<sub>Location: `features/steps/example.py:10`</sub>

✅ **When** the response payload matches the schema — `260ms` (Passed)

<sub>Location: `features/steps/example.py:11`</sub>

✅ **Given** the user opens the dashboard — `1.18s` (Passed)

<sub>Location: `features/steps/example.py:12`</sub>

✅ **And** the cart contains 7 items — `796ms` (Passed)

<sub>Location: `features/steps/example.py:13`</sub>

❌ **When** they click the login button — `1.16s` (Failed)

<sub>Location: `features/steps/example.py:14`</sub>

> **AssertionError**  
> Expected 200 but got 500

```python
Traceback (most recent call last):
  File "features/steps/example.py", line 42, in step_impl
    assert response.status_code == 200
AssertionError: Expected 200 but got 500
```

⚠️ **Given** the user opens the dashboard — `65ms` (Undefined)

<sub>Location: `features/steps/example.py:15`</sub>

</details>

<details>
<summary>⚠️ Scenario: Scenario 5: API contract</summary>

**Status:** ⚠️ Undefined

**Duration:** 540ms

**Location:** `features/Authentication.feature:20`

**Tags:** `wip`

##### Steps

✅ **Given** the response payload matches the schema — `148ms` (Passed)

<sub>Location: `features/steps/example.py:10`</sub>

⚠️ **When** the cart contains 1 items — `103ms` (Undefined)

<sub>Location: `features/steps/example.py:11`</sub>

⚠️ **Then** the API returns 200 — `290ms` (Undefined)

<sub>Location: `features/steps/example.py:12`</sub>

</details>

<details>
<summary>✅ Scenario: Scenario 6: checkout</summary>

**Status:** ✅ Passed

**Duration:** 4.56s

**Location:** `features/Authentication.feature:24`

**Tags:** `ui` `nightly`

##### Steps

✅ **Given** the user opens the dashboard — `647ms` (Passed)

<sub>Location: `features/steps/example.py:10`</sub>

⏭ **Then** the user opens the dashboard — `1.06s` (Skipped)

<sub>Location: `features/steps/example.py:11`</sub>

✅ **Then** the cart contains 8 items — `846ms` (Passed)

<sub>Location: `features/steps/example.py:12`</sub>

⏭ **Given** the API returns 200 — `1.12s` (Skipped)

<sub>Location: `features/steps/example.py:13`</sub>

✅ **When** the user opens the dashboard — `892ms` (Passed)

<sub>Location: `features/steps/example.py:14`</sub>

</details>

<details>
<summary>✅ Scenario: Scenario 7: checkout</summary>

**Status:** ✅ Passed

**Duration:** 2.13s

**Location:** `features/Authentication.feature:28`

##### Steps

✅ **Then** the API returns 200 — `1.09s` (Passed)

<sub>Location: `features/steps/example.py:10`</sub>

✅ **Given** the API returns 200 — `58ms` (Passed)

<sub>Location: `features/steps/example.py:11`</sub>

✅ **When** they click the buy button — `891ms` (Passed)

<sub>Location: `features/steps/example.py:12`</sub>

⏭ **And** the user opens the dashboard — `95ms` (Skipped)

<sub>Location: `features/steps/example.py:13`</sub>

</details>

<details>
<summary>✅ Scenario: Scenario 8: login flow</summary>

**Status:** ✅ Passed

**Duration:** 3.31s

**Location:** `features/Authentication.feature:32`

**Tags:** `regression` `wip` `api`

##### Steps

✅ **And** the API returns 200 — `441ms` (Passed)

<sub>Location: `features/steps/example.py:10`</sub>

✅ **Then** the user opens the dashboard — `428ms` (Passed)

<sub>Location: `features/steps/example.py:11`</sub>

⏭ **And** they click the buy button — `1.04s` (Skipped)

<sub>Location: `features/steps/example.py:12`</sub>

✅ **And** the API returns 200 — `940ms` (Passed)

<sub>Location: `features/steps/example.py:13`</sub>

✅ **When** the user opens the dashboard — `462ms` (Passed)

<sub>Location: `features/steps/example.py:14`</sub>

</details>

</details>

<details>
<summary>Feature: Reporting</summary>

> Behavior of the reporting subsystem.

Tags: `reporting`

#### [Reporting](#feature-reporting)

<details>
<summary>✅ Scenario: Scenario 1: permissions</summary>

**Status:** ✅ Passed

**Duration:** 2.77s

**Location:** `features/Reporting.feature:4`

**Tags:** `ui`

##### Steps

✅ **When** the response payload matches the schema — `397ms` (Passed)

<sub>Location: `features/steps/example.py:10`</sub>

✅ **Then** the response payload matches the schema — `817ms` (Passed)

<sub>Location: `features/steps/example.py:11`</sub>

⏭ **Then** the API returns 200 — `218ms` (Skipped)

<sub>Location: `features/steps/example.py:12`</sub>

✅ **Given** the API returns 200 — `876ms` (Passed)

<sub>Location: `features/steps/example.py:13`</sub>

✅ **And** the user opens the dashboard — `465ms` (Passed)

<sub>Location: `features/steps/example.py:14`</sub>

</details>

<details>
<summary>✅ Scenario: Scenario 2: API contract</summary>

**Status:** ✅ Passed

**Duration:** 1.91s

**Location:** `features/Reporting.feature:8`

**Tags:** `wip` `regression` `ui`

##### Steps

✅ **When** the user opens the dashboard — `1.14s` (Passed)

<sub>Location: `features/steps/example.py:10`</sub>

✅ **Then** the API returns 200 — `611ms` (Passed)

<sub>Location: `features/steps/example.py:11`</sub>

✅ **Then** the cart contains 5 items — `157ms` (Passed)

<sub>Location: `features/steps/example.py:12`</sub>

</details>

<details>
<summary>⚠️ Scenario: Scenario 3: checkout</summary>

**Status:** ⚠️ Undefined

**Duration:** 2.98s

**Location:** `features/Reporting.feature:12`

##### Steps

✅ **Then** the response payload matches the schema — `944ms` (Passed)

<sub>Location: `features/steps/example.py:10`</sub>

✅ **And** they click the submit button — `616ms` (Passed)

<sub>Location: `features/steps/example.py:11`</sub>

✅ **Given** the cart contains 9 items — `406ms` (Passed)

<sub>Location: `features/steps/example.py:12`</sub>

✅ **Then** they click the login button — `34ms` (Passed)

<sub>Location: `features/steps/example.py:13`</sub>

✅ **And** the response payload matches the schema — `500ms` (Passed)

<sub>Location: `features/steps/example.py:14`</sub>

⚠️ **When** the response payload matches the schema — `483ms` (Undefined)

<sub>Location: `features/steps/example.py:15`</sub>

</details>

<details>
<summary>✅ Scenario: Scenario 4: permissions</summary>

**Status:** ✅ Passed

**Duration:** 1.87s

**Location:** `features/Reporting.feature:16`

**Tags:** `regression` `api` `nightly`

##### Steps

✅ **When** the response payload matches the schema — `65ms` (Passed)

<sub>Location: `features/steps/example.py:10`</sub>

✅ **Given** the response payload matches the schema — `803ms` (Passed)

<sub>Location: `features/steps/example.py:11`</sub>

⏭ **Then** the response payload matches the schema — `998ms` (Skipped)

<sub>Location: `features/steps/example.py:12`</sub>

</details>

<details>
<summary>✅ Scenario: Scenario 5: permissions</summary>

**Status:** ✅ Passed

**Duration:** 4.18s

**Location:** `features/Reporting.feature:20`

##### Steps

✅ **And** the API returns 200 — `531ms` (Passed)

<sub>Location: `features/steps/example.py:10`</sub>

✅ **When** the API returns 200 — `1.07s` (Passed)

<sub>Location: `features/steps/example.py:11`</sub>

✅ **When** the response payload matches the schema — `834ms` (Passed)

<sub>Location: `features/steps/example.py:12`</sub>

✅ **Given** the API returns 200 — `653ms` (Passed)

<sub>Location: `features/steps/example.py:13`</sub>

✅ **Given** the response payload matches the schema — `1.09s` (Passed)

<sub>Location: `features/steps/example.py:14`</sub>

</details>

<details>
<summary>✅ Scenario: Scenario 6: API contract</summary>

**Status:** ✅ Passed

**Duration:** 4.00s

**Location:** `features/Reporting.feature:24`

**Tags:** `smoke` `api`

##### Steps

✅ **Then** the cart contains 7 items — `898ms` (Passed)

<sub>Location: `features/steps/example.py:10`</sub>

⏭ **When** the API returns 200 — `526ms` (Skipped)

<sub>Location: `features/steps/example.py:11`</sub>

✅ **And** they click the submit button — `1.01s` (Passed)

<sub>Location: `features/steps/example.py:12`</sub>

✅ **Given** the user opens the dashboard — `773ms` (Passed)

<sub>Location: `features/steps/example.py:13`</sub>

✅ **And** the API returns 200 — `458ms` (Passed)

<sub>Location: `features/steps/example.py:14`</sub>

✅ **And** the response payload matches the schema — `338ms` (Passed)

<sub>Location: `features/steps/example.py:15`</sub>

</details>

</details>

<details>
<summary>Feature: Settings</summary>

> Behavior of the settings subsystem.

Tags: `settings`

#### [Settings](#feature-settings)

<details>
<summary>✅ Scenario: Scenario 1: permissions</summary>

**Status:** ✅ Passed

**Duration:** 1.27s

**Location:** `features/Settings.feature:4`

##### Steps

✅ **When** the user opens the dashboard — `906ms` (Passed)

<sub>Location: `features/steps/example.py:10`</sub>

✅ **When** they click the login button — `156ms` (Passed)

<sub>Location: `features/steps/example.py:11`</sub>

✅ **When** the API returns 200 — `206ms` (Passed)

<sub>Location: `features/steps/example.py:12`</sub>

</details>

<details>
<summary>✅ Scenario: Scenario 2: API contract</summary>

**Status:** ✅ Passed

**Duration:** 3.63s

**Location:** `features/Settings.feature:8`

##### Steps

✅ **Given** the response payload matches the schema — `1.13s` (Passed)

<sub>Location: `features/steps/example.py:10`</sub>

✅ **Given** the user opens the dashboard — `838ms` (Passed)

<sub>Location: `features/steps/example.py:11`</sub>

✅ **Given** the API returns 200 — `642ms` (Passed)

<sub>Location: `features/steps/example.py:12`</sub>

✅ **Given** the user opens the dashboard — `1.02s` (Passed)

<sub>Location: `features/steps/example.py:13`</sub>

</details>

<details open>
<summary>❌ Scenario: Scenario 3: API contract</summary>

**Status:** ❌ Failed

**Duration:** 4.11s

**Location:** `features/Settings.feature:12`

**Tags:** `nightly` `regression` `api`

##### Steps

❌ **When** the cart contains 3 items — `1.16s` (Failed)

<sub>Location: `features/steps/example.py:10`</sub>

> **AssertionError**  
> Expected 200 but got 500

```python
Traceback (most recent call last):
  File "features/steps/example.py", line 42, in step_impl
    assert response.status_code == 200
AssertionError: Expected 200 but got 500
```

✅ **And** the cart contains 7 items — `326ms` (Passed)

<sub>Location: `features/steps/example.py:11`</sub>

✅ **Given** they click the submit button — `902ms` (Passed)

<sub>Location: `features/steps/example.py:12`</sub>

⚠️ **And** the response payload matches the schema — `1.02s` (Undefined)

<sub>Location: `features/steps/example.py:13`</sub>

✅ **And** the API returns 200 — `412ms` (Passed)

<sub>Location: `features/steps/example.py:14`</sub>

✅ **Given** the user opens the dashboard — `293ms` (Passed)

<sub>Location: `features/steps/example.py:15`</sub>

</details>

<details>
<summary>⚠️ Scenario: Scenario 4: checkout</summary>

**Status:** ⚠️ Undefined

**Duration:** 2.38s

**Location:** `features/Settings.feature:16`

**Tags:** `smoke` `nightly`

##### Steps

✅ **Given** the response payload matches the schema — `832ms` (Passed)

<sub>Location: `features/steps/example.py:10`</sub>

✅ **Then** the cart contains 9 items — `416ms` (Passed)

<sub>Location: `features/steps/example.py:11`</sub>

⏭ **Then** the API returns 200 — `371ms` (Skipped)

<sub>Location: `features/steps/example.py:12`</sub>

✅ **Given** the API returns 200 — `148ms` (Passed)

<sub>Location: `features/steps/example.py:13`</sub>

⏭ **When** the response payload matches the schema — `335ms` (Skipped)

<sub>Location: `features/steps/example.py:14`</sub>

⚠️ **Then** the API returns 200 — `277ms` (Undefined)

<sub>Location: `features/steps/example.py:15`</sub>

</details>

</details>

---

## Environment

| Variable          | Value                                  |
| ----------------- | -------------------------------------- |
| Python version    | 3.12.1                                 |
| Behave version    | 1.2.6                                  |
| Operating system  | Demo OS 1.0 (x86_64)                   |
| Hostname          | demo-host                              |
| Working directory | `/demo/project`                        |
| Execution command | `behave -f markdown -o demo-report.md` |
| User              | demo-user                              |
| CPU count         | 8                                      |
| Memory (MB)       | 16384                                  |
| Git branch        | main                                   |
| Git commit        | a1b2c3d                                |
| Git remote        | https://github.com/demo/project.git    |

### CI / Environment Variables

| Variable | Value         |
| -------- | ------------- |
| CI       | false         |
| HOME     | /home/demo    |
| PATH     | /usr/bin:/bin |
| SHELL    | /bin/bash     |

---

*Report generated by Behave Markdown Report — Demo on 2026-06-29 20:09:10.*
