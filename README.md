# stats

Small helpers on top of [Pingouin](https://pingouin-stats.org/) for common tests (t-tests, correlations, ANOVA, etc.).

## Installation

Install from GitHub (not published on PyPI):

```bash
pip install "git+https://github.com/fangzefunny/stats.git"
```

Pin a branch or tag by appending `@branch-or-tag` to the URL.

## Usage

```python
from stats import stats

stats.anova(dv="y", between="group", data=df)
```

You can also import functions directly: `from stats import anova, t_test`.
