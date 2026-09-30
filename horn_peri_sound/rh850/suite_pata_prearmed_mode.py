import vlab

from common import VlabTestCase
from pata_constants import (PerimeterAlarmCfgM2, VehPwMdeStat,
                            LifeCycMdeDActl, OnChangeInfiniteTimerStatus,
                            ExteriorVehicleLockStatus, LastLockUnlockRequestor, ExteriorLockEventCount)


class PreArmedMode(VlabTestCase):
    """
    This class holds the test case for PATA - PreArmed Mode.
    """
    # Default elf file to use when it is not provided from slash or CI/CD
    ELF_FILENAME = "PerimeterAlrmVehMdeNewTrgEvnt.elf"

    def before(self, args):
        super(PreArmedMode, self).before(args)
        self.initialize()

    def after(self, args):
        super(PreArmedMode, self).after(args)

        vlab.exit()

    def initialize(self):

        self.step("Calling Init function")
        vlab.call_software("RePerimeterAlrmVehMdeNewTrgEvntInit", blocking=True)

    def test_prearmed_mode(self, args):
        """
        This is to test that the vehicle is entering to Perimeter Alarm PRE-ARMED mode properly or not:
        https://ford.atlassian.net/browse/ZOPRO-26897
        https://ford.atlassian.net/browse/ZOPRO-22338
        """
        (perimeter_alrmcfgm2, lifecycmd, vehpwmde, onchg_tmrstat, extvehlckstat,
         lst_lck_unlck_rqstr, ext_lck_evnt_cnt, alrmstat) = args.inputs.split("-")

        perimeter_alrmcfgm2_val = PerimeterAlarmCfgM2.from_str(perimeter_alrmcfgm2)
        lifecycmd_val = LifeCycMdeDActl.from_str(lifecycmd)
        vehpwmde_val = VehPwMdeStat.from_str(vehpwmde)
        onchg_tmrstat_val = OnChangeInfiniteTimerStatus.from_str(onchg_tmrstat)
        extvehlckstat_val = ExteriorVehicleLockStatus.from_str(extvehlckstat)
        lst_lck_unlck_rqstr_val = LastLockUnlockRequestor.from_str(lst_lck_unlck_rqstr)
        ext_lck_evnt_cnt_val = ExteriorLockEventCount.from_str(ext_lck_evnt_cnt)

        self.step("Checking the alarm status ")
        self.verify_perimetere_alarm_disarmed()

        self.step("set PerimeterAlarmCfgM2 = {}".format(perimeter_alrmcfgm2_val))
        self.memory.write("PerimeterAlrmVehMdeNewTrgEvnt_NvmCczmDE10PerimeterAlarmCfgM2",
                          perimeter_alrmcfgm2_val, 'Boolean')

        self.step("set LifeCycMdeDActl = {}".format(lifecycmd_val))
        self.memory.write("Rte_PerimeterAlrmVehMdeNewTrgEvnt_LifeCycleMode_Val",
                          lifecycmd_val, 'uint8')

        self.step("set VehPwMdeStat = {}".format(vehpwmde_val))
        self.memory.write("Rte_PerimeterAlrmVehMdeNewTrgEvnt_VehPwMdeStat_Grp", vehpwmde_val, 'uint8')

        self.step("set onChange_infiniteTimerStatus =  {}".format(onchg_tmrstat_val))
        self.memory.write("Rte_PerimeterAlrmVehMdeNewTrgEvnt_onChange_infiniteTimerStatusInterface_"
                          "onChange_infiniteTimerStatus", onchg_tmrstat_val,
                          'uint8')

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
        self.call_10ms_runnable_multiple_times(3)

        if alrmstat == "prearm":
            self.verify_perimetere_alarm_prearmed()
        else:
            self.verify_perimetere_alarm_disarmed()
