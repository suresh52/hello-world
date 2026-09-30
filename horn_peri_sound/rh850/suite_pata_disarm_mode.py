import vlab

from common import VlabTestCase
from pata_constants import (CommonStrings, VehPwMdeStat, LifeCycMdeDActl, ExteriorVehicleLockStatus,
                            LastLockUnlockRequestor, ExteriorLockEventCount, ExteriorDoorHandleStatus)


class DisArmedMode(VlabTestCase):
    """
    This class holds the test case for PATA - DisArmed Mode.
    """
    # Default elf file to use when it is not provided from slash or CI/CD
    ELF_FILENAME = "PerimeterAlrmVehMdeNewTrgEvnt.elf"

    def before(self, args):
        super(DisArmedMode, self).before(args)
        self.initialize()

    def after(self, args):
        super(DisArmedMode, self).after(args)

        vlab.exit()

    def initialize(self):

        self.step("Calling Init function")
        vlab.call_software("RePerimeterAlrmVehMdeNewTrgEvntInit", blocking=True)

    def test_disarmed_mode_with_lifecyclemode(self, args):
        """
        This is to test the disarmed mode
        Requirement ID: https://ford.atlassian.net/browse/ZOPRO-26899
        """
        lifecyclemode = args.inputs
        alrmstat = args.outputs
        lifecyclemode_val = LifeCycMdeDActl.from_str(lifecyclemode)

        self.step(CommonStrings.setting_prearmed_mode_str)
        self.set_prearmed_mode()

        self.step("Set LifeCycMdeDActl  = {}".format(lifecyclemode_val))
        self.memory.write("Rte_PerimeterAlrmVehMdeNewTrgEvnt_LifeCycleMode_Val", lifecyclemode_val, 'uint8')
        self.call_10ms_runnable_multiple_times(2)

        if alrmstat == 'disarm':
            self.verify_perimetere_alarm_disarmed()
        else:
            self.verify_perimetere_alarm_prearmed()

    def test_disarmed_mode_with_vehiclepowermode(self, args):
        """
        This is to test the disarmed mode
        Requirement ID: https://ford.atlassian.net/browse/ZOPRO-26899
        """
        vehpwmdestat = args.inputs
        alrmstat = args.outputs
        vehpwmdestat_val = VehPwMdeStat.from_str(vehpwmdestat)

        self.step(CommonStrings.setting_prearmed_mode_str)
        self.set_prearmed_mode()

        self.step("Set VehPwMdeStat  = {}".format(vehpwmdestat_val))
        self.memory.write("Rte_PerimeterAlrmVehMdeNewTrgEvnt_VehPwMdeStat_Grp", vehpwmdestat_val, 'uint8')
        self.call_10ms_runnable_multiple_times(2)

        if alrmstat == 'disarm':
            self.verify_perimetere_alarm_disarmed()
        else:
            self.verify_perimetere_alarm_prearmed()

    def test_disarmed_mode_with_exteriorvehiclelockstatus(self, args):
        """
        This is to test the disarmed mode
        Requirement ID: https://ford.atlassian.net/browse/ZOPRO-26899
        """
        (precondition, extvehlckstat, lst_lck_unlck_rqstr) = args.inputs.split("::")
        alrmstat = args.outputs

        extvehlckstat_val = ExteriorVehicleLockStatus.from_str(extvehlckstat)
        lst_lck_unlck_rqstr_val = LastLockUnlockRequestor.from_str(lst_lck_unlck_rqstr)

        if precondition == "prearm":
            self.step(CommonStrings.setting_prearmed_mode_str)
            self.set_prearmed_mode()
        elif precondition == "arm":
            self.step(CommonStrings.setting_armed_mode_str)
            self.set_armed_mode()
        else:
            self.step("Setting the alarm status to ACTIVATED")
            self.set_activated_mode()

        self.step("Setting exteriorVehicleLockStatus=  {}".format(extvehlckstat_val))
        self.memory.write("Rte_PerimeterAlrmVehMdeNewTrgEvnt_exteriorVehicleLockStatus_"
                          "onChange_exteriorVehicleLockStatus", extvehlckstat_val,
                          'uint8')

        self.step("Setting lastLockUnlockRequestor =  {}".format(lst_lck_unlck_rqstr_val))
        self.memory.write("Rte_PerimeterAlrmVehMdeNewTrgEvnt_lastLockUnlockRequestor_onChange_lastLockUnlockRequestor",
                          lst_lck_unlck_rqstr_val, 'uint8')

        self.call_10ms_runnable_multiple_times(2)

        if alrmstat == 'disarm':
            self.verify_perimetere_alarm_disarmed()
        elif alrmstat == 'prearm':
            self.verify_perimetere_alarm_prearmed()
        elif alrmstat == 'arm':
            self.verify_perimetere_alarm_armed()
        else:
            self.verify_perimetere_alarm_activated()

    def test_disarmed_mode_with_patilaly_locked(self, args):
        """
        This is to test the disarmed mode
        Requirement ID: https://ford.atlassian.net/browse/ZOPRO-26899
        """
        (precondition, extvehlckstat, ext_lck_evnt_cnt, ext_doorhandle_status, alrmstat) = args.inputs.split("-")

        extvehlckstat_val = ExteriorVehicleLockStatus.from_str(extvehlckstat)
        ext_lck_evnt_cnt_val = ExteriorLockEventCount.from_str(ext_lck_evnt_cnt)
        ext_doorhandle_status_val = ExteriorDoorHandleStatus.from_str(ext_doorhandle_status)

        dr_list = [0, 1, 2, 3]

        if precondition == "prearm":
            self.step(CommonStrings.setting_prearmed_mode_str)
            self.set_prearmed_mode()
        elif precondition == "arm":
            self.step(CommonStrings.setting_armed_mode_str)
            self.set_armed_mode()
        else:
            self.step("Setting the alarm status to ACTIVATED")
            self.set_activated_mode()

        self.step("Setting exteriorVehicleLockStatus=  {}".format(extvehlckstat_val))
        self.memory.write("Rte_PerimeterAlrmVehMdeNewTrgEvnt_exteriorVehicleLockStatus_"
                          "onChange_exteriorVehicleLockStatus", extvehlckstat_val,
                          'uint8')

        self.step("Setting exteriorLockEventCount = {}".format(ext_lck_evnt_cnt_val))
        self.memory.write("Rte_PerimeterAlrmVehMdeNewTrgEvnt_exteriorLockEventCount_onChange_exteriorLockEventCount",
                          ext_lck_evnt_cnt_val, 'uint8')

        for drid in dr_list:
            self.memory.write(CommonStrings.ext_door_handle_variable.format(drid), ext_doorhandle_status_val, 'uint8')

        self.call_10ms_runnable_multiple_times(2)

        if alrmstat == 'disarm':
            self.verify_perimetere_alarm_disarmed()
        elif alrmstat == 'prearm':
            self.verify_perimetere_alarm_prearmed()
        elif alrmstat == 'arm':
            self.verify_perimetere_alarm_armed()
        else:
            self.verify_perimetere_alarm_activated()
