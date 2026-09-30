import vlab

from common import VlabTestCase
from pata_constants import (ExteriorVehicleLockStatus, LastLockUnlockRequestor,
                            ExteriorLockEventCount)


class ArmedMode(VlabTestCase):
    """
    This class holds the test case for PATA - Armed Mode.
    """
    # Default elf file to use when it is not provided from slash or CI/CD
    ELF_FILENAME = "PerimeterAlrmVehMdeNewTrgEvnt.elf"

    def before(self, args):
        super(ArmedMode, self).before(args)
        self.initialize()

    def after(self, args):
        super(ArmedMode, self).after(args)

        vlab.exit()

    def initialize(self):

        self.step("Calling Init function")
        vlab.call_software("RePerimeterAlrmVehMdeNewTrgEvntInit", blocking=True)

    def test_armed_mode_with_exteriorvehiclelockstatus(self, args):
        """
        This is to test that the vehicle is entering to Perimeter Alarm ARMED mode properly or not:
        https://ford.atlassian.net/browse/ZOPRO-26896
        """
        (extvehlckstat, lst_lck_unlck_rqstr, ext_lck_evnt_cnt) = args.inputs.split("::")
        alrmstat = args.outputs

        extvehlckstat_val = ExteriorVehicleLockStatus.from_str(extvehlckstat)
        lst_lck_unlck_rqstr_val = LastLockUnlockRequestor.from_str(lst_lck_unlck_rqstr)
        ext_lck_evnt_cnt_val = ExteriorLockEventCount.from_str(ext_lck_evnt_cnt)

        self.step("Setting the alarm status to ACTIVATED")
        self.set_activated_mode()

        self.step("Setting exteriorVehicleLockStatus=  {}".format(extvehlckstat_val))
        self.memory.write("Rte_PerimeterAlrmVehMdeNewTrgEvnt_exteriorVehicleLockStatus_"
                          "onChange_exteriorVehicleLockStatus", extvehlckstat_val,
                          'uint8')

        self.step("Setting lastLockUnlockRequestor =  {}".format(lst_lck_unlck_rqstr_val))
        self.memory.write("Rte_PerimeterAlrmVehMdeNewTrgEvnt_lastLockUnlockRequestor_onChange_lastLockUnlockRequestor",
                          lst_lck_unlck_rqstr_val, 'uint8')

        self.step("Setting exteriorLockEventCount = {}".format(ext_lck_evnt_cnt_val))
        self.memory.write("Rte_PerimeterAlrmVehMdeNewTrgEvnt_exteriorLockEventCount_onChange_exteriorLockEventCount",
                          ext_lck_evnt_cnt_val, 'uint8')
        self.call_10ms_runnable_multiple_times(2)

        if alrmstat == "arm":
            self.verify_perimetere_alarm_armed()
        elif alrmstat == "disarm":
            self.verify_perimetere_alarm_disarmed()
        else:
            self.verify_perimetere_alarm_activated()

    def test_armed_mode_with_alarmcycle_complettion(self, args):
        """
        This is to test that the vehicle is entering to Perimeter Alarm ARMED mode properly or not:
        Requirement ID: https://ford.atlassian.net/browse/ZOPRO-26896
        """

        (timer, doorajaratatus) = args.inputs.split("::")
        timer = int(timer)

        self.step("Setting the alarm status to ACTIVATED")
        self.set_activated_mode()

        self.memory.write("Rte_PerimeterAlrmVehMdeNewTrgEvnt_TmrSecCnt_DeVal", timer, "uint32")
        self.call_10ms_runnable_multiple_times(2)

        if timer >= 305:
            self.verify_perimetere_alarm_armed()
        else:
            self.verify_perimetere_alarm_activated()
