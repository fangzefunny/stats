# stats

Small helpers on top of [Pingouin](https://pingouin-stats.org/) for common tests (t-tests, correlations, ANOVA, etc.).

## Installation

Install from GitHub (not published on PyPI):

```bash
pip install "git+https://github.com/fangzefunny/stats.git"
```

Pin a branch or tag by appending `@branch-or-tag` to the URL.

## Usage

Import the package and call helpers on the module (recommended):

```python
import stats

stats.t_test(x, y, paired=False, title="Group A vs B")
stats.anova(dv="y", between="group", data=df)
```

Equivalent: import the bundled namespace object (same callables):

```python
from stats import stats

stats.t_test(x, y)
stats.anova(dv="y", between="group", data=df)
```

You can also import callables directly: `from stats import anova, t_test`.
