"""Contains the test for PATA - Intrusion and Inclination
"""
import slash
from ..tests_barmetal_rh850_generic_base import Rh850Base


# Test functions defined within this class will be used for traceability with testrail.
class TestIntrusionInclination(Rh850Base):
    """
    This class holds the test case for PATA - Intrusion and Inclination .
    """

    common_intru_incli_inp = [
         "bth-null-unlck-clsd-arm-trig-arm",
         "bth-null-na-clsd-arm-trig-arm",
         "bth-null-fal-clsd-arm-trig-arm",
         "bth-null-lck-ajar-arm-trig-arm",
         "bth-null-lck-fal-arm-trig-arm",
         "bth-null-lck-unk-arm-trig-arm",
         "bth-null-lck-na-arm-trig-arm",
         "bth-null-lck-clsd-disarm-trig-act",
         "bth-null-lck-clsd-unk-trig-act",
         "bth-null-lck-clsd-arm-not_trig-arm"
     ]
    intrusion_sensing_inputs = [
        "bth-null-lck-clsd-arm-trig-act",
        "intru-null-lck-clsd-arm-trig-act",
        "none-null-lck-clsd-arm-trig-arm",
        "incli-null-lck-clsd-arm-trig-arm",
        "iri-null-lck-clsd-arm-trig-arm",
        "bri-null-lck-clsd-arm-trig-arm",
        "intru-off-lck-clsd-arm-trig-act",
        "intru-persis-lck-clsd-arm-trig-arm",
        "intru-on-lck-clsd-arm-trig-arm",
    ]

    @slash.parametrize('intrusion_sensing_inputs',
                       intrusion_sensing_inputs + common_intru_incli_inp)
    def test_arming_intrusion_sensing(self, intrusion_sensing_inputs):
        """
        Run Test - test_arming_intrusion_sensing
        https://ford.atlassian.net/browse/ZOPRO-26900
        https://ford.atlassian.net/browse/ZOPRO-26702
        https://ford.atlassian.net/browse/ZOPRO-22318
        https://ford.atlassian.net/browse/ZOPRO-22374
        https://ford.atlassian.net/browse/ZOPRO-22372
        https://ford.atlassian.net/browse/ZOPRO-22371
        """

        result = self.execute_vlab_test("test_arming_intrusion_sensing",
                                        inputs=intrusion_sensing_inputs)
        self._assert_return_code(result)

    inclination_sensing_inputs = [
         "bth-null-lck-clsd-arm-trig-act",
         "incli-null-lck-clsd-arm-trig-act",
         "none-null-lck-clsd-arm-trig-arm",
         "intru-null-lck-clsd-arm-trig-arm",
         "iri-null-lck-clsd-arm-trig-arm",
         "bri-null-lck-clsd-arm-trig-arm",
         "incli-off-lck-clsd-arm-trig-act",
         "incli-persis-lck-clsd-arm-trig-arm",
         "incli-on-lck-clsd-arm-trig-arm",
    ]

    @slash.parametrize('inclination_sensig_inputs',
                       inclination_sensing_inputs + common_intru_incli_inp)
    def test_arming_inclination_sensing(self, inclination_sensig_inputs):
        """
        Run Test - test_arming_inclination_sensing
        https://ford.atlassian.net/browse/ZOPRO-26903
        https://ford.atlassian.net/browse/ZOPRO-26702
        https://ford.atlassian.net/browse/ZOPRO-22318
        https://ford.atlassian.net/browse/ZOPRO-22372
        https://ford.atlassian.net/browse/ZOPRO-22309
        """

        result = self.execute_vlab_test("test_arming_inclination_sensing",
                                        inputs=inclination_sensig_inputs)
        self._assert_return_code(result)

    intrusion_disarm_state_inputs = ['False', 'True']

    @slash.parametrize('trigger', intrusion_disarm_state_inputs)
    def test_intrusion_disarm_state_with_securitycfgm2(self, trigger):
        """
        Run Test - test_intrusion_disarm_state_with_securitycfgm2
        https://ford.atlassian.net/browse/ZOPRO-22373
        https://ford.atlassian.net/browse/ZOPRO-26902
        """
        result = self.execute_vlab_test("test_intrusion_disarm"
                                        "_state_with_securitycfgm2", inputs=trigger)
        self._assert_return_code(result)

    @slash.parametrize('trigger', intrusion_disarm_state_inputs)
    def test_intrusion_disarm_state_with_alarm_disarmed(self, trigger):
        """
        Run Test - test_intrusion_disarm_state_with_alarm_disarmed
        https://ford.atlassian.net/browse/ZOPRO-22373
        https://ford.atlassian.net/browse/ZOPRO-26902
        """
        result = self.execute_vlab_test("test_intrusion_disarm_state_with_alarm_disarmed",
                                        inputs=trigger)
        self._assert_return_code(result)

    @slash.parametrize('trigger', intrusion_disarm_state_inputs)
    def test_intrusion_disarm_state_with_extdoorhandlestatus(self, trigger):
        """
        Run Test - test_intrusion_disarm_state_with_extdoorhandlestatus
        https://ford.atlassian.net/browse/ZOPRO-22373
        https://ford.atlassian.net/browse/ZOPRO-26902
        """
        result = self.execute_vlab_test("test_intrusion_disarm_state_with_extdoorhandlestatus",
                                        inputs=trigger)
        self._assert_return_code(result)

    intrusion_disarm_state_inputs_2 = [('arm', 'False'),
                                       ('act', 'True')
                                       ]

    @slash.parametrize(('alarmstat', 'trigger'), intrusion_disarm_state_inputs_2)
    def test_intrusion_disarm_state_with_climateairflowlvl(self, alarmstat, trigger):
        """
        Run Test - test_intrusion_disarm_state_with_climateairflowlvl
        https://ford.atlassian.net/browse/ZOPRO-22373
        https://ford.atlassian.net/browse/ZOPRO-26902
        """
        result = self.execute_vlab_test("test_intrusion_disarm_state_with_climateairflowlvl",
                                        inputs=f"{alarmstat}::{trigger}")
        self._assert_return_code(result)

    intrusion_disarm_state_inputs_2 = ['df', 'dr', 'pf', 'pr', 'bec']

    @slash.parametrize('doorid', intrusion_disarm_state_inputs_2)
    def test_intrusion_disarm_state_with_doorajarstatus(self, doorid):
        """
        Run Test - test_intrusion_disarm_state_with_doorajarstatus
        https://ford.atlassian.net/browse/ZOPRO-22373
        https://ford.atlassian.net/browse/ZOPRO-26902
        """
        result = self.execute_vlab_test("test_intrusion_disarm_"
                                        "state_with_doorajarstatus", inputs=doorid)
        self._assert_return_code(result)

    intru_incli_reset_behaviour_inputs = [
        ('intru', 'trig'),
        ('intru', 'not_trig'),
        ('incli', 'trig'),
        ('incli', 'not_trig'),
    ]

    @slash.parametrize(('trigger_name', 'std'), intru_incli_reset_behaviour_inputs)
    def test_intru_incli_reset_behavior(self, trigger_name, std):
        """
            Run Test - test_intru_incli_reset_behavior
            https://ford.atlassian.net/browse/ZOPRO-22308
        """
        result = self.execute_vlab_test("test_intru_incli_reset_behavior",
                                        inputs=f"{trigger_name}::{std}")
        self._assert_return_code(result)
