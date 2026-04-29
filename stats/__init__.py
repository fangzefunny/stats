"""Pingouin-based helpers for common statistical tests.

Use either style:

- ``import stats`` then ``stats.t_test(...)``, ``stats.anova(...)``, etc.
- ``from stats import stats`` then ``stats.t_test(...)`` (same functions on a
  :class:`~types.SimpleNamespace` for a single import target).
"""

import types

import pingouin as pg

__all__ = [
    "stats",
    "t_test",
    "mwu",
    "wilcoxon",
    "corr",
    "partial_corr",
    "anova",
    "linear_regression",
]


def t_test(x, y, paired=False, alternative="two-sided", title="", p_bar=0.05):
    df = pg.ttest(x, y, paired=paired, alternative=alternative)
    dof = df.loc[:, "dof"].values[0]
    t = df.loc[:, "T"].values[0]
    pval = df.loc[:, "p-val"].values[0]
    cohen_d = df.loc[:, "cohen-d"].values[0]
    ci = df.loc[:, "CI95%"].values[0]
    pair_str = "-paired" if paired else ""
    if pval <= p_bar:
        print(
            f"{title} \tt{pair_str}({dof:.3f})={t:.3f}, p={pval:.3f}, "
            f"cohen-d={cohen_d:.3f}, 95% CI={ci}"
        )
    return df


def mwu(x, y, alternative="two-sided", title="", p_bar=0.05):
    df = pg.mwu(x, y, alternative=alternative)
    n = df.shape[0]
    U = df.loc[:, "U-val"].values[0]
    pval = df.loc[:, "p-val"].values[0]
    CLES = df.loc[:, "CLES"].values[0]
    if pval <= p_bar:
        print(f"{title} \tU({n})={U:.3f}, p={pval:.3f}, CLES={CLES:.3f}")
    return df


def wilcoxon(x, y, alternative="two-sided", title="", p_bar=0.05):
    df = pg.wilcoxon(x, y, alternative=alternative)
    n = x.shape[0]
    W = df.loc[:, "W-val"].values[0]
    pval = df.loc[:, "p-val"].values[0]
    CLES = df.loc[:, "CLES"].values[0]
    if pval <= p_bar:
        print(f"{title} \tW({n})={W:.3f}, p={pval:.3f}, CLES={CLES:.3f}")
    return df


def corr(x, y, method="pearson", title="", p_bar=0.05):
    df = pg.corr(x, y, method=method)
    n = df.loc[:, "n"].values[0]
    r = df.loc[:, "r"].values[0]
    pval = df.loc[:, "p-val"].values[0]
    ci = df.loc[:, "CI95%"].values[0]
    if method == "pearson":
        rstr = "r"
    elif method == "spearman":
        rstr = "rho"
    elif method == "kendall":
        rstr = "tau"
    else:
        rstr = ""
    if pval <= p_bar:
        print(f"{title} \t{rstr}({n})={r:.3f}, p={pval:.3f}, 95% CI={ci}")
    return df


def partial_corr(data, x, y, covar, method="pearson", title="", p_bar=0.05):
    df = pg.partial_corr(
        data=data, x=x, y=y, covar=covar, method=method
    )
    n = df.loc[:, "n"].values[0]
    r = df.loc[:, "r"].values[0]
    pval = df.loc[:, "p-val"].values[0]
    ci = df.loc[:, "CI95%"].values[0]
    if pval <= p_bar:
        print(f"{title} \tr({n})={r:.3f}, p={pval:.3f}, 95% CI={ci}")
    return df


def anova(dv, between, data, all_table=False, p_bar=0.05):
    df = pg.anova(dv=dv, between=between, data=data).rename(
        columns={"p-unc": "punc"}
    )
    sig_df = df if all_table else df.query(f"punc<={p_bar}")
    dof2 = int(df["DF"].values[-1])
    for _, row in sig_df.iterrows():
        title = row["Source"]
        dof1 = int(row["DF"])
        F = row["F"]
        p = row["punc"]
        np2 = row["np2"]
        print(f"\t{title}:\tF({dof1}, {dof2})={F:.3f}, p={p:.3f}, np2={np2:.3f}")
    if not all_table:
        other_df = df.query("punc>.05")
        if other_df.shape[0] > 0:
            other_min_p = other_df["punc"].min()
            print(f"\tOther: \tp>={other_min_p:.3f}")
    return df


def linear_regression(
    x,
    y,
    add_intercept=False,
    title="",
    x_var="x",
    y_var="y",
    remove_na=False,
    p_bar=0.05,
):
    df = pg.linear_regression(
        X=x, y=y, add_intercept=add_intercept, remove_na=remove_na
    )
    beta0 = df["coef"][0]
    beta1 = df["coef"][1]
    pval = df["pval"][1]
    if pval <= p_bar:
        print(
            f"{title}\t{y_var}={beta1:.3f}{x_var}+{beta0:.3f},\n\tp={pval:.3f}"
        )
    return df


stats = types.SimpleNamespace(
    **{name: globals()[name] for name in __all__ if name != "stats"}
)
