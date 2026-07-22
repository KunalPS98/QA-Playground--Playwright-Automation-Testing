# QA Playground - Playwright Automation Testing

Test automation suite for [QA Playground](https://qa-playground-automation-testing.onrender.com/)
([source](https://github.com/KunalPS98/qa-playground)), a demo storefront built for practicing UI,
API, and data-validation testing. The app ships with a set of intentional bugs (see its `BUGS.md`);
this suite documents each one as a `strict` `xfail` test rather than ignoring it.

## Stack

- Python + [pytest](https://docs.pytest.org/)
- [Playwright](https://playwright.dev/python/) for browser automation (UI + admin tests)
- [requests](https://requests.readthedocs.io/) for HTTP-level API tests
- [pytest-bdd](https://pytest-bdd.readthedocs.io/) for Gherkin-style scenarios
- [Allure](https://allurereport.org/) + `pytest-html` for reporting

## Project structure

```
pages/          Page Object Model - one class per page/component, no assertions
api/            Domain-specific API client (QAPlaygroundApiClient)
utils/          Shared test data helpers (unique users, seeded sample accounts)
features/       Gherkin .feature files (BDD scenarios)
tests/
  test_*.py       UI tests (registration, login, catalog, cart, checkout, admin)
  api/            API tests (auth, products, orders, users) - no browser involved
  bdd/            Step definitions wiring features/*.feature to the same page objects
conftest.py     Shared fixtures (new_user, registered_page, admin_page, allure attachments)
pytest.ini      base-url, screenshot/video/trace-on-failure, markers, BDD feature dir
```

## Setup

```powershell
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
playwright install chromium
```

## Running tests

All commands below assume the venv is activated (`venv\Scripts\activate`) - your prompt
should show `(venv)`. If it isn't activated, prefix any command with `venv\Scripts\python.exe -m`
(e.g. `venv\Scripts\python.exe -m pytest`) instead of running `pytest` directly.

```powershell
# everything
pytest

# one layer at a time
pytest tests/test_*.py tests/test_admin.py -v   # UI + admin
pytest tests/api -v                            # API only, no browser
pytest tests/bdd -v                            # BDD only

# by marker
pytest -m smoke      # fast, high-value happy paths
pytest -m bug        # known-bug regression tests only

# watch the browser instead of running headless
pytest --headed
```

Expect **25 passed, 11 xfailed** on a full run. The `xfail`s are not failures - they're
`strict=True` tests documenting real, confirmed bugs in the app (see each test's `reason=`).
If one ever unexpectedly passes (`XPASS`), that means the underlying bug was fixed and the
test/marker should be revisited.

## Reports

`pytest.ini` always writes `reports/report.html` (pytest-html) and `reports/allure-results/`
(Allure) for whatever subset of tests you just ran. Failure screenshots, videos, and traces are
captured automatically and attached to the Allure report.

```powershell
# view the plain HTML report
start reports/report.html

# generate + open the Allure report
allure generate reports/allure-results -o reports/allure-report --clean
allure open reports/allure-report
```

To keep a layer's report separate from the others, override the paths on the command line
(last value wins over `pytest.ini`'s defaults):

```powershell
pytest tests/api --html=reports/api-report.html --self-contained-html --alluredir=reports/allure-results-api
```

Debugging a failed test's trace:

```powershell
playwright show-trace reports/artifacts/<test-slug>/trace.zip
```

## CI

`.github/workflows/tests.yml` runs the full suite on every push/PR to `main`/`master`: installs
dependencies, installs the Chromium browser, runs `pytest`, and uploads the HTML report, Allure
results, and any failure screenshots/videos/traces as workflow artifacts - even when tests fail
(`if: always()`).

## Design notes

- **Page Object Model**: page objects hold locators and actions only; every assertion lives in
  the test. `HeaderComponent` is a standalone component (not tied to one URL) since the nav bar
  appears on every page.
- **Test isolation**: UI/admin tests that need an account use `registered_page` /
  `new_user`, which register a fresh, `uuid`-suffixed user per test - no shared mutable state
  between runs. API tests follow the same idea via `new_api_user` and `created_products`,
  cleaning up whatever they create through the admin client.
- **API client**: `QAPlaygroundApiClient` exposes one named method per endpoint
  (`create_order`, `update_product`, ...) rather than generic `get`/`post` wrappers - the API
  equivalent of a Page Object.
- **BDD**: `tests/bdd/` step definitions call the exact same page objects as the plain UI tests -
  Gherkin is a presentation layer here, not a separate automation implementation.
