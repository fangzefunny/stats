"""Ensure public import paths for the stats package API."""

import unittest


class TestImportPaths(unittest.TestCase):
    def test_import_stats_module_uses_t_test(self):
        import stats

        self.assertTrue(callable(stats.t_test))
        self.assertTrue(callable(stats.anova))

    def test_from_stats_import_stats_matches_module(self):
        import stats as stats_pkg
        from stats import stats as stats_ns

        self.assertIs(stats_pkg.t_test, stats_ns.t_test)
        self.assertIs(stats_pkg.anova, stats_ns.anova)


if __name__ == "__main__":
    unittest.main()
