import vlab

from common import VlabTestCase
from pata_constants import (DrAjarStatus, DrID, CommonStrings, PrmtrAlrmEvntDStat, TrailerConnection,
                            TrailerAlarmActivation, OnChangeTrailerAlarmSetting, TrailerConnectCfgM2)


class ActivatedMode(VlabTestCase):
    """
    This class holds the test case for PATA - Activated Mode.
    """
    # Default elf file to use when it is not provided from slash or CI/CD
    ELF_FILENAME = "PerimeterAlrmVehMdeNewTrgEvnt.elf"

    def before(self, args):
        super(ActivatedMode, self).before(args)
        self.initialize()

    def after(self, args):
        super(ActivatedMode, self).after(args)

        vlab.exit()

    def initialize(self):

        self.step("Calling Init function")
        vlab.call_software("RePerimeterAlrmVehMdeNewTrgEvntInit", blocking=True)

    def test_activated_mode_with_doorajarstatus(self, args):
        """
        This is to test that the vehicle is entering to Perimeter Alarm ACTIVATED mode properly or not:
        Requirement ID: https://ford.atlassian.net/browse/ZOPRO-26702
                        https://ford.atlassian.net/browse/ZOPRO-11348
                        https://ford.atlassian.net/browse/ZOPRO-26898
                        https://ford.atlassian.net/browse/ZOPRO-11351
                        https://ford.atlassian.net/browse/ZOPRO-22330
                        https://ford.atlassian.net/browse/ZOPRO-22325
                        https://ford.atlassian.net/browse/ZOPRO-22335

        """

        (doorid, doorajarstatus, perimeter_event_stat) = args.inputs.split("::")
        alrmstat = args.outputs

        doorid_val = DrID.from_str(doorid)
        doorajarstatus_val = DrAjarStatus.from_str(doorajarstatus)
        perimeter_event_stat_val = PrmtrAlrmEvntDStat.from_str(perimeter_event_stat)

        self.step(CommonStrings.setting_prearmed_mode_str)
        self.set_prearmed_mode()

        self.step(CommonStrings.setting_armed_mode_str)
        self.set_armed_mode()

        self.step(CommonStrings.setting_doorajarstatus_str.format(doorid_val, doorajarstatus_val))
        self.memory.write(CommonStrings.door_ajar_status_variable.format(doorid_val), doorajarstatus_val, 'uint8')
        self.call_10ms_runnable_multiple_times(3)
        event_trigger_val = self.memory.read("Rte_PerimeterAlrmVehMdeNewTrgEvnt_PrmtrAlrmEvntDStat_Val", 'uint8')

        self.verify_equal(event_trigger_val, perimeter_event_stat_val)

        if alrmstat == "act":
            self.verify_perimetere_alarm_activated()
        else:
            self.verify_perimetere_alarm_armed()

    def test_activated_mode_with_trailer_diconnected(self, args):
        """
        This is to test that the vehicle is entering to Perimeter Alarm ACTIVATED mode properly or not:
        Requirement ID: https://ford.atlassian.net/browse/ZOPRO-26702
        """
        trailerconnection = args.inputs
        alrmstat = args.outputs
        trailerconnection_val = TrailerConnection.from_str(trailerconnection)

        self.step("Setting the PATrailerConnectCfgM2  to ENABLED")
        self.memory.write("PerimeterAlrmVehMdeNewTrgEvnt_NvmCczmPATrailerConnectCfgM2", TrailerConnectCfgM2.ENABLED,
                          'Boolean')

        self.step("Setting the Trailer connection = YES")
        self.memory.write(
            "Rte_PerimeterAlrmVehMdeNewTrgEvnt_onChange_trailerConnectionInterface_onChange_trailerConnection",
            trailerconnection_val, 'uint8')
        self.call_10ms_runnable_multiple_times()

        self.step(CommonStrings.setting_prearmed_mode_str)
        self.set_prearmed_mode()

        self.step(CommonStrings.setting_armed_mode_str)
        self.set_armed_mode()

        self.step("Arming trailer Alarm")
        self.memory.write("Rte_PerimeterAlrmVehMdeNewTrgEvnt_onChange_trailerAlarmSetting_onChange_trailerAlarmSetting",
                          OnChangeTrailerAlarmSetting.TrailerConnectionAlarmSetting_ON, 'uint8')
        self.call_10ms_runnable_multiple_times()
        trailer_alarm_stat = self.memory.read("Rte_PerimeterAlrmVehMdeNewTrgEvnt_onChange_"
                                              "trailerAlarmInterface_onChange_trailerAlarm", "uint8")
        self.step(CommonStrings.checking_trailer_alarm_str)
        self.verify_equal(trailer_alarm_stat, TrailerAlarmActivation.TrailerAlarmActivation_TRAILER_ALARM_ACTIVE)

        self.step("onChangeTrailerConnection = {}".format(trailerconnection))
        self.memory.write("Rte_PerimeterAlrmVehMdeNewTrgEvnt_onChange_"
                          "trailerConnectionInterface_onChange_trailerConnection",
                          TrailerConnection.TrailerConnection_TRAILER_CONNECTION_NO, 'uint8')

        self.call_10ms_runnable_multiple_times(3)

        if alrmstat == 'act':
            self.verify_perimetere_alarm_activated()
        else:
            self.verify_perimetere_alarm_armed()
