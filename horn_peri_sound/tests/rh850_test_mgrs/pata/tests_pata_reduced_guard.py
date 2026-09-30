"""Contains the test for PATA - ReducedGuard Mode
"""
import slash
from ..tests_barmetal_rh850_generic_base import Rh850Base


# Test functions defined within this class will be used for traceability with testrail.
class TestReduceGuard(Rh850Base):
    """
    This class holds the test case for PATA - ReducedGuard Mode.
    """

    reduce_guard_inputs = [
        ('persis', 'persis'),
        ('on', 'on'),
        ('null', 'off'),
        ('off', 'off')]

    @slash.parametrize(('rg_val', 'rg_stat'), reduce_guard_inputs)
    def test_reduced_guard_on(self, rg_val, rg_stat):
        """
        Run Test - test_reduced_guard_on
        https://ford.atlassian.net/browse/ZOPRO-26901
        """

        result = self.execute_vlab_test("test_reduced_guard_on",
                                        inputs=f"{rg_val}", outputs=f"{rg_stat}",)
        self._assert_return_code(result)

    def test_reduced_guard_off(self):
        """
        Run Test - test_reduced_guard_off
        https://ford.atlassian.net/browse/ZOPRO-22312
        """
        result = self.execute_vlab_test("test_reduced_guard_off")
        self._assert_return_code(result)

    reduced_guard_off_inputs = [
        ('vpm60', 'off'),
        ('vpm70', 'off'),
        ('vpm10', 'on'),
        ('vpm20', 'on'),
        ('vpm40', 'on'),
        ('vpm50', 'on'),

    ]

    @slash.parametrize(('vpm', 'reducedguard_stat'), reduced_guard_off_inputs)
    def test_reduced_guard_off_with_vehpwrmode(self, vpm, reducedguard_stat):
        """
        Run Test - test_reduced_guard_off_with_vehpwrmode
        https://ford.atlassian.net/browse/ZOPRO-22312
        """
        result = self.execute_vlab_test("test_reduced_guard_off_with_vehpwrmode",
                                        inputs=f"{vpm}::{reducedguard_stat}")
        self._assert_return_code(result)
