---
title: 'pytest: helps you write better programs¶'
source: https://docs.pytest.org/en/stable/
published: '2015-01-01'
site: docs.pytest.org
clipped: '2026-08-27'
---

# pytest: helps you write better programs¶

# pytest: helps you write better programs[¶](#pytest-helps-you-write-better-programs)

The `pytest` framework makes it easy to write small, readable tests, and can
scale to support complex functional testing for applications and libraries.

**PyPI package name**: [pytest](https://pypi.org/project/pytest)

## A quick example[¶](#a-quick-example)

```
# content of test_sample.py
def inc(x):
    return x + 1
def test_answer():
    assert inc(3) == 5
```
To execute it:

```
$ pytest
=========================== test session starts ============================
platform linux -- Python 3.x.y, pytest-9.x.y, pluggy-1.x.y
rootdir: /home/sweet/project
collected 1 item
test_sample.py F                                                     [100%]
================================= FAILURES =================================
_______________________________ test_answer ________________________________
    def test_answer():
>       assert inc(3) == 5
E       assert 4 == 5
E        +  where 4 = inc(3)
test_sample.py:6: AssertionError
========================= short test summary info ==========================
FAILED test_sample.py::test_answer - assert 4 == 5
============================ 1 failed in 0.12s =============================
```
Due to `pytest`’s detailed assertion introspection, only plain `assert` statements are used.
See [Get started](getting-started.html#getstarted) for a basic introduction to using pytest.

## Features[¶](#id1)

- Detailed info on failing [assert statements](how-to/assert.html#assert) (no need to remember`self.assert*` names)
- [Auto-discovery](explanation/goodpractices.html#test-discovery) of test modules and functions
- [Modular fixtures](reference/fixtures.html#fixture) for managing small or parametrized long-lived test resources
- Can run [unittest](how-to/unittest.html#unittest) (including trial) test suites out of the box
- Python 3.10+ or PyPy 3
- Rich plugin architecture, with over 1300+ [external plugins](reference/plugin_list.html#plugin-list) and thriving community

## Documentation[¶](#documentation)

- [Get started](getting-started.html#get-started) - install pytest and grasp its basics in just twenty minutes
- [How-to guides](how-to/index.html#how-to) - step-by-step guides, covering a vast range of use-cases and needs
- [Reference guides](reference/index.html#reference) - includes the complete pytest API reference, lists of plugins and more
- [Explanation](explanation/index.html#explanation) - background, discussion of key topics, answers to higher-level questions

## Bugs/Requests[¶](#bugs-requests)

Please use the [GitHub issue tracker](https://github.com/pytest-dev/pytest/issues) to submit bugs or request features.

## Support pytest[¶](#support-pytest)

[Open Collective](https://opencollective.com) is an online funding platform for open and transparent communities.
It provides tools to raise money and share your finances in full transparency.

It is the platform of choice for individuals and companies that want to make one-time or monthly donations directly to the project.

See more details in the [pytest collective](https://opencollective.com/pytest).

## pytest for enterprise[¶](#pytest-for-enterprise)

Available as part of the Tidelift Subscription.

The maintainers of pytest and thousands of other packages are working with Tidelift to deliver commercial support and maintenance for the open source dependencies you use to build your applications. Save time, reduce risk, and improve code health, while paying the maintainers of the exact dependencies you use.

### Security[¶](#security)

If you have found an issue that you believe is a security vulnerability, please do not create an issue – instead, report it via a [new security advisory](https://github.com/pytest-dev/pytest/security/advisories/new).
