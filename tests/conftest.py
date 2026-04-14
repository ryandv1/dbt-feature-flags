"""pytest configuration for dbt-feature-flags tests.

Handles dbt version differences that affect test setup:

- dbt 1.5 added MACRO_DEBUGGING to the global flags Namespace.  Without
  calling set_from_args() the attribute is absent, which causes an
  AttributeError inside dbt's jinja._compile() when tests render templates.
  We set it to False (the correct default for non-debug runs) before the
  test session starts.
"""


def pytest_configure(config) -> None:
    """Seed missing dbt flag attributes required by dbt 1.5+."""
    try:
        from dbt.flags import get_flags  # only present in dbt 1.5+

        flags = get_flags()
        if not hasattr(flags, "MACRO_DEBUGGING"):
            flags.MACRO_DEBUGGING = False
    except Exception:
        # Older dbt versions do not expose get_flags — nothing to do.
        pass
