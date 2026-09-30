import vlab

from common import VlabTestCase
from pata_constants import (CommonStrings, TrailerAlarmActivation,
                            OnChangeTrailerAlarmSetting, TrailerConnectCfgM2, LifeCycMdeDActl,
                            OnChangeTrailerAlarmTimer, TrailerConnection)


class TrailerAlarm(VlabTestCase):
    """
    This class holds the test case for PATA - Trailer Alarm.
    """
    # Default elf file to use when it is not provided from slash or CI/CD
    ELF_FILENAME = "PerimeterAlrmVehMdeNewTrgEvnt.elf"

    def before(self, args):
        super(TrailerAlarm, self).before(args)
        self.initialize()

    def after(self, args):
        super(TrailerAlarm, self).after(args)

        vlab.exit()

    def initialize(self):

        self.step("Calling Init function")
        vlab.call_software("RePerimeterAlrmVehMdeNewTrgEvntInit", blocking=True)

    def test_arming_trailer_alarm(self, args):
        """
        This is to test that the trailer alarm is arming or not:
        Requirement ID: https://ford.atlassian.net/browse/ZOPRO-26705
                https://ford.atlassian.net/browse/ZOPRO-26703
        """
        (trailerconnectcfgm2, lifecycmde, trailer_alarm_setting) = args.inputs.split("::")
        alrmstat = args.outputs

        trailerconnectcfgm2_val = TrailerConnectCfgM2.from_str(trailerconnectcfgm2)
        lifecycmde_val = LifeCycMdeDActl.from_str(lifecycmde)
        trailer_alarm_setting_val = OnChangeTrailerAlarmSetting.from_str(trailer_alarm_setting)

        self.step(CommonStrings.setting_prearmed_mode_str)
        self.set_prearmed_mode()

        self.step(CommonStrings.setting_armed_mode_str)
        self.set_armed_mode()

        self.step("Setting TrailerConnectCfgM2 = {}")
        self.memory.write("PerimeterAlrmVehMdeNewTrgEvnt_NvmCczmPATrailerConnectCfgM2", trailerconnectcfgm2_val,
                          'Boolean')

        self.step("Setting LifeCycMdeDActl = {}")
        self.memory.write("Rte_PerimeterAlrmVehMdeNewTrgEvnt_LifeCycleMode_Val", lifecycmde_val, 'uint8')

        self.step("Setting OnChangeTrailerAlarmSetting = {}")
        self.memory.write("Rte_PerimeterAlrmVehMdeNewTrgEvnt_onChange_trailerAlarmSetting_"
                          "onChange_trailerAlarmSetting", trailer_alarm_setting_val, 'uint8')

        self.call_10ms_runnable_multiple_times()

        trailer_alarm_stat = self.memory.read("Rte_PerimeterAlrmVehMdeNewTrgEvnt_onChange_trailerAlarmInterface_"
                                              "onChange_trailerAlarm", "uint8")

        if alrmstat == "act":
            self.verify_equal(trailer_alarm_stat, TrailerAlarmActivation.TrailerAlarmActivation_TRAILER_ALARM_ACTIVE)
        else:
            self.verify_equal(trailer_alarm_stat, TrailerAlarmActivation.TrailerAlarmActivation_TRAILER_ALARM_INACTIVE)

    def test_trailer_kol_behaviour(self, args):
        """
        This is to test the trailer_kol_behaviour:
        Requirement ID: https://ford.atlassian.net/browse/ZOPRO-26704
        """

        (trailer_alarm_timer, trailerconnection, alarmstat) = args.inputs.split("::")
        trailer_alarm_timer_val = OnChangeTrailerAlarmTimer.from_str(trailer_alarm_timer)
        trailerconnection_val = TrailerConnection.from_str(trailerconnection)

        self.step(CommonStrings.setting_trailer_alarm_armed_str)
        self.set_trailer_alarm_armed()

        self.step("set onChange_trailerAlarmTimer = RUN")
        self.memory.write("Rte_PerimeterAlrmVehMdeNewTrgEvnt_onChange_trailerAlarmTimerInterface"
                          "_onChange_trailerAlarmTimer", OnChangeTrailerAlarmTimer.RUN, 'uint8')

        self.step("Set onChange_trailerAlarmTimer = END")
        self.memory.write("Rte_PerimeterAlrmVehMdeNewTrgEvnt_onChange_trailerAlarmTimerInterface"
                          "_onChange_trailerAlarmTimer", trailer_alarm_timer_val, 'uint8')

        self.step("onChange_trailerConnection = No")
        self.memory.write(
            "Rte_PerimeterAlrmVehMdeNewTrgEvnt_onChange_trailerConnectionInterface_onChange_trailerConnection",
            trailerconnection_val, 'uint8')
        self.call_10ms_runnable_multiple_times(3)

        self.check_alarm(alarmstatus=alarmstat)

    def test_disarming_trailer_alarm_with_traileralarmsetting(self, args):
        """
        This is to test the disarming trailer alarm:
        Requirement ID: https://ford.atlassian.net/browse/ZOPRO-26708
        """

        (pre_alarmstate, trailer_alarm_setting, traileralarm_stat,) = args.inputs.split("::")
        trailer_alarm_setting_val = OnChangeTrailerAlarmSetting.from_str(trailer_alarm_setting)

        self.step(CommonStrings.setting_trailer_alarm_armed_str)
        self.set_trailer_alarm_armed()

        if pre_alarmstate == "act":
            self.set_activated_mode()
        self.step("set the trailerAlarmSetting = OFF")
        self.memory.write("Rte_PerimeterAlrmVehMdeNewTrgEvnt_onChange_trailerAlarmSetting_onChange_trailerAlarmSetting",
                          trailer_alarm_setting_val, 'uint8')
        self.call_10ms_runnable_multiple_times()

        trailer_alarm_stat = self.memory.read("Rte_PerimeterAlrmVehMdeNewTrgEvnt_onChange_"
                                              "trailerAlarmInterface_onChange_trailerAlarm", "uint8")
        self.step(CommonStrings.checking_trailer_alarm_str)
        if traileralarm_stat == "inactive":
            self.verify_equal(trailer_alarm_stat, TrailerAlarmActivation.TrailerAlarmActivation_TRAILER_ALARM_INACTIVE)
        else:
            self.verify_equal(trailer_alarm_stat, TrailerAlarmActivation.TrailerAlarmActivation_TRAILER_ALARM_ACTIVE)

    def test_disarming_trailer_alarm_with_disarmed_mode(self, args):
        """
        This is to test the disarming trailer alarm:
        Requirement ID: https://ford.atlassian.net/browse/ZOPRO-26708
        """
        self.step(CommonStrings.setting_trailer_alarm_armed_str)
        self.set_trailer_alarm_armed()

        self.step("set the perimeter alarm to disarmed state")
        self.set_disarmed_mode()
        trailer_alarm_stat = self.memory.read("Rte_PerimeterAlrmVehMdeNewTrgEvnt_onChange_"
                                              "trailerAlarmInterface_onChange_trailerAlarm", "uint8")
        self.verify_equal(trailer_alarm_stat, TrailerAlarmActivation.TrailerAlarmActivation_TRAILER_ALARM_INACTIVE)
