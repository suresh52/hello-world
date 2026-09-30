import vlab

from common import VlabTestCase
from pata_constants import (CommonStrings, DrID, DrAjarStatus, Timer)


class IndividualTriggerAlarm(VlabTestCase):
    """
    This class holds the test case for PATA - Individual Trigger Armed Mode.
    """
    # Default elf file to use when it is not provided from slash or CI/CD
    ELF_FILENAME = "PerimeterAlrmVehMdeNewTrgEvnt.elf"

    def before(self, args):
        super(IndividualTriggerAlarm, self).before(args)
        self.initialize()

    def after(self, args):
        super(IndividualTriggerAlarm, self).after(args)

        vlab.exit()

    def initialize(self):

        self.step("Calling Init function")
        vlab.call_software("RePerimeterAlrmVehMdeNewTrgEvntInit", blocking=True)

    def test_individual_trigger_armed_mode(self, args):
        """
        This is to test that the Driver Door - Individual Trigger Armed State:
        Requirement ID: https://ford.atlassian.net/browse/ZOPRO-11350
                This is to test that the Driver Rear  Door - Individual Trigger Armed State:
        Requirement ID: https://ford.atlassian.net/browse/ZOPRO-22321
                This is to test that the Passenger Door - Individual Trigger Armed State:
        Requirement ID: https://ford.atlassian.net/browse/ZOPRO-22326
                This is to test that the Passenger Rear Door - Individual Trigger Armed State:
        Requirement ID: https://ford.atlassian.net/browse/ZOPRO-22331
        """

        (precondition_alarmstat, delaytimer, doorid, door_ajar_status_1, door_ajar_status_2,
         alrmstat1, alrmstat2) = args.inputs.split("-")

        doorid_val = DrID.from_str(doorid)
        door_ajar_status_1_val = DrAjarStatus.from_str(door_ajar_status_1)
        door_ajar_status_2_val = DrAjarStatus.from_str(door_ajar_status_2)

        if precondition_alarmstat == 'prearm':
            self.step(CommonStrings.setting_prearmed_mode_str)
            self.set_prearmed_mode()

            self.step(CommonStrings.setting_doorajarstatus_str.format(doorid_val, door_ajar_status_1_val))
            self.memory.write(CommonStrings.door_ajar_status_variable.format(doorid_val), door_ajar_status_1_val,
                              'uint8')
            self.call_10ms_runnable_multiple_times(3)

        if delaytimer == '20':
            tmr_sec_cnt = Timer.INITIAL_TIMER
            while tmr_sec_cnt < Timer.ARMING_DELAY_TIMER:
                self.memory.write("Rte_PerimeterAlrmVehMdeNewTrgEvnt_TmrSecCnt_DeVal", tmr_sec_cnt, "uint32")
                self.call_10ms_runnable_multiple_times()
                if precondition_alarmstat == 'prearm':
                    self.verify_perimetere_alarm_prearmed()
                else:
                    self.verify_perimetere_alarm_disarmed()
                tmr_sec_cnt += 10
            self.memory.write("Rte_PerimeterAlrmVehMdeNewTrgEvnt_TmrSecCnt_DeVal", tmr_sec_cnt, "uint32")
            self.call_10ms_runnable_multiple_times()
        else:
            tmr_sec_cnt = Timer.INITIAL_TIMER
            while tmr_sec_cnt < 15:
                self.memory.write("Rte_PerimeterAlrmVehMdeNewTrgEvnt_TmrSecCnt_DeVal", tmr_sec_cnt, "uint32")
                self.call_10ms_runnable_multiple_times()
                self.verify_perimetere_alarm_prearmed()
                tmr_sec_cnt += 5

        self.check_alarm(alarmstatus=alrmstat1)

        self.step(CommonStrings.setting_doorajarstatus_str.format(doorid_val, door_ajar_status_2_val))
        self.memory.write(CommonStrings.door_ajar_status_variable.format(doorid_val), door_ajar_status_2_val,
                          'uint8')
        self.call_10ms_runnable_multiple_times(3)

        self.check_alarm(alarmstatus=alrmstat2)

    def test_individual_trigger_armed_mode_2(self, args):
        """
        Requirement ID: https://ford.atlassian.net/browse/ZOPRO-11350
        This is to test that the Driver Rear  Door - Individual Trigger Armed State:
        Requirement ID: https://ford.atlassian.net/browse/ZOPRO-22321
        This is to test that the Passenger Door - Individual Trigger Armed State:
        Requirement ID: https://ford.atlassian.net/browse/ZOPRO-22326
        This is to test that the Passenger Rear Door - Individual Trigger Armed State:
        Requirement ID: https://ford.atlassian.net/browse/ZOPRO-22331
        """

        (doorid, door_ajar_status) = args.inputs.split("::")
        doorid_val = DrID.from_str(doorid)
        door_ajar_status_val = DrAjarStatus.from_str(door_ajar_status)

        self.step(CommonStrings.setting_doorajarstatus_str.format(doorid_val, door_ajar_status_val))
        self.memory.write(CommonStrings.door_ajar_status_variable.format(doorid_val), door_ajar_status_val, 'uint8')
        self.call_10ms_runnable_multiple_times(3)

        self.step(CommonStrings.setting_prearmed_mode_str)
        self.set_prearmed_mode()

        tmr_sec_cnt = Timer.INITIAL_TIMER
        while tmr_sec_cnt < Timer.ARMING_DELAY_TIMER:
            self.memory.write("Rte_PerimeterAlrmVehMdeNewTrgEvnt_TmrSecCnt_DeVal", tmr_sec_cnt, "uint32")
            self.call_10ms_runnable_multiple_times()
            self.verify_perimetere_alarm_prearmed()
            tmr_sec_cnt += 10
        self.memory.write("Rte_PerimeterAlrmVehMdeNewTrgEvnt_TmrSecCnt_DeVal", tmr_sec_cnt, "uint32")
        self.call_10ms_runnable_multiple_times()

        self.step("Set doorAjarStatus[{}] = AJAR".format(doorid_val))
        self.memory.write("Rte_PerimeterAlrmVehMdeNewTrgEvnt_doorAjarStatus_onChange_doorAjarStatus[{}]"
                          .format(doorid_val), DrAjarStatus.AJAR, 'uint8')
        self.call_10ms_runnable_multiple_times(3)
        # Alarm should not get activated with AJAR trigger because door trigger will be in disarmed mode.

        self.step(CommonStrings.checking_alarm_status_str)
        self.verify_perimetere_alarm_armed()
