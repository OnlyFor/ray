import click
from typing import List

from ci.ray_ci.utils import ci_init
from ci.ray_ci.automation.determine_microcheck_tests import LINUX_TEST_PREFIX
from ray_release.test import Test


@click.command()
def main() -> None:
    """
    This script determines the rayci step ids to run microcheck tests.
    """
    ci_init()
    step_ids = _get_high_impact_step_ids(Test.gen_from_s3(prefix=LINUX_TEST_PREFIX))
    print(",".join([step for step in step_ids if step]))


def _get_high_impact_step_ids(tests: List[Test]) -> List[str]:
    high_impact_tests = [test for test in tests if test.is_high_impact()]
    return [
        test.get_test_results(limit=1)[0].rayci_step_id for test in high_impact_tests
    ]


if __name__ == "__main__":
    main()
