"""Contains the test for PATA - Individual Trigger Armed Mode.
"""
import slash
from ..tests_barmetal_rh850_generic_base import Rh850Base


# Test functions defined within this class will be used for traceability with testrail.
class TestIndividualTriggerArmedMode(Rh850Base):
    """
    This class holds the test case for PATA - Individual Trigger Armed Mode.
    """

    individual_door_trigger_armed_inputs = [
        'prearm-20-df-clsd-ajar-arm-act',
        'disarm-20-df-clsd-ajar-disarm-disarm',
        'prearm-15-df-clsd-ajar-prearm-prearm',
        'prearm-20-dr-clsd-ajar-arm-act',
        'disarm-20-dr-clsd-ajar-disarm-disarm',
        'prearm-15-dr-clsd-ajar-prearm-prearm',
        'prearm-20-pf-clsd-ajar-arm-act',
        'disarm-20-pf-clsd-ajar-disarm-disarm',
        'prearm-15-pf-clsd-ajar-prearm-prearm',
        'prearm-20-pr-clsd-ajar-arm-act',
        'disarm-20-pr-clsd-ajar-disarm-disarm',
        'prearm-15-pr-clsd-ajar-prearm-prearm'
    ]

    @slash.parametrize('door_trigger_armed_inputs',
                       individual_door_trigger_armed_inputs)
    def test_individual_trigger_armed_mode(self, door_trigger_armed_inputs):
        """
        Run Test - test_individual_trigger_armed_mode

        Requirement ID: https://ford.atlassian.net/browse/ZOPRO-11350
        Requirement ID: https://ford.atlassian.net/browse/ZOPRO-22321
        Requirement ID: https://ford.atlassian.net/browse/ZOPRO-22326
        Requirement ID: https://ford.atlassian.net/browse/ZOPRO-22331
        """

        result = self.execute_vlab_test("test_individual_trigger_armed_mode",
                                        inputs=door_trigger_armed_inputs)
        self._assert_return_code(result)

    individual_door_trigger_armed_inputs_2 = [
        ('df', 'ajar'),
        ('df', 'fal'),
        ('df', 'unk'),
        ('df', 'na'),
        ('dr', 'ajar'),
        ('dr', 'fal'),
        ('dr', 'unk'),
        ('dr', 'na'),
        ('pf', 'ajar'),
        ('pf', 'fal'),
        ('pf', 'unk'),
        ('pf', 'na'),
        ('pr', 'ajar'),
        ('pr', 'fal'),
        ('pr', 'unk'),
        ('pr', 'na')
    ]

    @slash.parametrize(('drid', 'das'), individual_door_trigger_armed_inputs_2)
    def test_individual_trigger_armed_mode_2(self, drid, das):
        """
        Run Test - test_individual_trigger_armed_mode
        Requirement ID: https://ford.atlassian.net/browse/ZOPRO-11350
        Requirement ID: https://ford.atlassian.net/browse/ZOPRO-22321
        Requirement ID: https://ford.atlassian.net/browse/ZOPRO-22326
        Requirement ID: https://ford.atlassian.net/browse/ZOPRO-22331
        """

        result = self.execute_vlab_test("test_individual_trigger_armed_mode_2",
                                        inputs=f"{drid}::{das}")
        self._assert_return_code(result)
