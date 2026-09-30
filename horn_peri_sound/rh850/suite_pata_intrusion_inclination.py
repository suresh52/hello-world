import vlab

from common import VlabTestCase
from pata_constants import (DrAjarStatus, DrID, SensorTriggeredData,
                            ExteriorDoorHandleStatus, SensorState, ReducedGuard, SecurityCfgM2, CommonStrings)


class IntrusionInclination(VlabTestCase):
    """
    This class holds the test case for PATA - Intrusion and Inclination .
    """
    # Default elf file to use when it is not provided from slash or CI/CD
    ELF_FILENAME = "PerimeterAlrmVehMdeNewTrgEvnt.elf"

    def before(self, args):
        super(IntrusionInclination, self).before(args)
        self.initialize()

    def after(self, args):
        super(IntrusionInclination, self).after(args)

        vlab.exit()

    def initialize(self):

        self.step("Calling Init function")
        vlab.call_software("RePerimeterAlrmVehMdeNewTrgEvntInit", blocking=True)

    def test_arming_intrusion_sensing(self, args):
        """
        This is to test arming_intrusion_sensing:
        https://ford.atlassian.net/browse/ZOPRO-26900
        https://ford.atlassian.net/browse/ZOPRO-26702
        https://ford.atlassian.net/browse/ZOPRO-22318
        https://ford.atlassian.net/browse/ZOPRO-22374
        https://ford.atlassian.net/browse/ZOPRO-22372
        https://ford.atlassian.net/browse/ZOPRO-22371
        """

        (securitycfgm2, reducedguard, ext_doorhandle_status, doorajaratatus,
         sensorstate, sensor_triggered_data, alrmstat) = args.inputs.split("-")

        securitycfgm2_val = SecurityCfgM2.from_str(securitycfgm2)
        reducedguard_val = ReducedGuard.from_str(reducedguard)
        ext_doorhandle_status_val = ExteriorDoorHandleStatus.from_str(ext_doorhandle_status)
        sensorstate_val = SensorState.from_str(sensorstate)
        sensor_triggered_data_val = SensorTriggeredData.from_str(sensor_triggered_data)
        doorajaratatus_val = DrAjarStatus.from_str(doorajaratatus)

        dr_list = [0, 1, 2, 3, 4, 5, 9]
        # driver door, passenger door, driver second row, passenger second row, bec, bec2, bec3
        self.step(CommonStrings.setting_prearmed_mode_str)
        self.set_prearmed_mode()

        self.step("Set SecurityCfgM2 = {}".format(securitycfgm2_val))
        self.memory.write("PerimeterAlrmVehMdeNewTrgEvnt_NvmCczmDE10SecurityCfgM2", securitycfgm2_val, 'uint8')

        self.step("Set ReducedGuardDreq  = {}".format(reducedguard_val))
        self.memory.write("Rte_PerimeterAlrmVehMdeNewTrgEvnt_ReducedGuardDRq_Val", reducedguard_val, 'uint8')

        self.step("Set exteriorDoorHandleStatus = {} and doorAjarStatus  = {}".format(ext_doorhandle_status_val,
                                                                                      doorajaratatus_val))
        for drid in dr_list:
            self.memory.write(CommonStrings.ext_door_handle_variable.format(drid), ext_doorhandle_status_val, 'uint8')

            self.memory.write(CommonStrings.door_ajar_status_variable.format(drid), doorajaratatus_val, 'uint8')

        self.step("Set onChange_climateAirFlwSettingInterface[18].ClimtAirFlowLvl  = 0")
        self.memory.write(CommonStrings.climate_airflow_lvl_var, 0, 'uint8')

        self.step(CommonStrings.setting_armed_mode_str)
        self.set_armed_mode()

        if sensorstate_val == 2 or sensorstate_val == 1 or sensor_triggered_data_val == 1 or securitycfgm2_val == 2:
            # SesorState = 2 (UNKNOWN) 1 (DISARMED)
            # SensorTriggeredData = 1 (Triggered)
            # SecurityCfgM2 = 3 (INCLINATION)
            self.step("Set InclinationStatus.SensorState = DISARMED")
            self.memory.write(CommonStrings.incli_sensor_state_var, SensorState.SensorStateEnum_DISARMED,
                              'uint8')

            self.step("Set  InclinationStatus.SensorTriggeredData = NOT TRIGGERED")
            self.memory.write(CommonStrings.incli_sensor_trig_data_var,
                              SensorTriggeredData.SensorTriggeredDataEnum_NOT_TRIGGERED, 'uint8')

        self.step("Set  intrusionStatus.SensorState = {}".format(sensorstate_val))
        self.memory.write(CommonStrings.intru_sensor_state_var, sensorstate_val, 'uint8')

        self.step("Set  IntrusionStatus.SensorTriggeredData = {}".format(sensor_triggered_data_val))
        self.memory.write(CommonStrings.intru_sensor_trig_data_var, sensor_triggered_data_val, 'uint8')

        self.call_10ms_runnable_multiple_times(2)

        if alrmstat == "act":
            self.verify_perimetere_alarm_activated()
        else:
            self.verify_perimetere_alarm_armed()

    def test_arming_inclination_sensing(self, args):
        """
        This is to test arming_inclination_sensing:
        https://ford.atlassian.net/browse/ZOPRO-26903
        https://ford.atlassian.net/browse/ZOPRO-26702
        https://ford.atlassian.net/browse/ZOPRO-22318
        https://ford.atlassian.net/browse/ZOPRO-22372
        https://ford.atlassian.net/browse/ZOPRO-22309
        """

        (securitycfgm2, reducedguard, ext_doorhandle_status, doorajaratatus,
         sensorstate, sensor_triggered_data, alrmstat) = args.inputs.split("-")

        securitycfgm2_val = SecurityCfgM2.from_str(securitycfgm2)
        reducedguard_val = ReducedGuard.from_str(reducedguard)
        ext_doorhandle_status_val = ExteriorDoorHandleStatus.from_str(ext_doorhandle_status)
        sensorstate_val = SensorState.from_str(sensorstate)
        sensor_triggered_data_val = SensorTriggeredData.from_str(sensor_triggered_data)
        doorajarstatus_val = DrAjarStatus.from_str(doorajaratatus)

        dr_list = [0, 1, 2, 3, 4, 5, 6, 9]
        # driver door, passenger door, driver second row, passenger second row, bec, bec2, bec3
        self.step(CommonStrings.setting_prearmed_mode_str)
        self.set_prearmed_mode()

        self.step("Set SecurityCfgM2 = {}".format(securitycfgm2_val))
        self.memory.write("PerimeterAlrmVehMdeNewTrgEvnt_NvmCczmDE10SecurityCfgM2", securitycfgm2_val, 'uint8')

        self.step("Set ReducedGuardDreq  = {}".format(reducedguard_val))
        self.memory.write("Rte_PerimeterAlrmVehMdeNewTrgEvnt_ReducedGuardDRq_Val", reducedguard_val, 'uint8')

        self.step("Set exteriorDoorHandleStatus = {} and Set doorAjarStatus  = {}"
                  .format(ext_doorhandle_status_val, doorajarstatus_val))
        for drid in dr_list:
            self.memory.write(CommonStrings.ext_door_handle_variable.format(drid), ext_doorhandle_status_val, 'uint8')

            self.memory.write(CommonStrings.door_ajar_status_variable.format(drid), doorajarstatus_val, 'uint8')

        self.step(CommonStrings.setting_armed_mode_str)
        self.set_armed_mode()

        if sensorstate_val == 2 or sensorstate_val == 1 or sensor_triggered_data_val == 1 or securitycfgm2_val == 3:
            # SesorState = 2 (UNKNOWN) 1 (DISARMED)
            # SensorTriggeredData = 1 (Triggered)
            # SecurityCfgM2 = 3 (INTRUSION)

            self.step("Set  intrusionStatus.SensorState = DISARMED")
            self.memory.write(CommonStrings.intru_sensor_state_var, SensorState.SensorStateEnum_DISARMED, 'uint8')

            self.step("Set  IntrusionStatus.SensorTriggeredData = NOT TRIGGERED")
            self.memory.write(CommonStrings.intru_sensor_trig_data_var, SensorTriggeredData.
                              SensorTriggeredDataEnum_NOT_TRIGGERED,
                              'uint8')

        self.step("Set  InclinationStatus.SensorState = {}".format(sensorstate_val))
        self.memory.write(CommonStrings.incli_sensor_state_var, sensorstate_val, 'uint8')

        self.step("Set  InclinationStatus.SensorTriggeredData = {}".format(sensor_triggered_data_val))
        self.memory.write(CommonStrings.incli_sensor_trig_data_var, sensor_triggered_data_val,
                          'uint8')
        self.call_10ms_runnable_multiple_times(2)

        if alrmstat == "act":
            self.verify_perimetere_alarm_activated()
        else:
            self.verify_perimetere_alarm_armed()

    def test_intrusion_disarm_state_with_securitycfgm2(self, args):
        """
        This is to test the Intrusion disarm state:
        Requirement ID: https://ford.atlassian.net/browse/ZOPRO-22373
        https://ford.atlassian.net/browse/ZOPRO-26902
        """
        trigger_val = args.inputs

        self.step(CommonStrings.setting_intrusion_armed_str)
        self.set_intrusion_armed_and_activate(trigger=trigger_val)

        self.step("set SecurityCfgM2 = Disabled")
        self.memory.write("PerimeterAlrmVehMdeNewTrgEvnt_NvmCczmDE10SecurityCfgM2",
                          SecurityCfgM2.SECURITYCFG_NONE, 'uint8')

        if trigger_val == 'True':
            self.finish_alarm_cycle()

        self.step(CommonStrings.setting_intrusion_triggered_str)
        self.memory.write(CommonStrings.intru_sensor_trig_data_var, SensorTriggeredData.
                          SensorTriggeredDataEnum_TRIGGERED, 'uint8')

        self.call_10ms_runnable_multiple_times()

        self.verify_perimeter_alarm_not_activated()

    def test_intrusion_disarm_state_with_alarm_disarmed(self, args):
        """
        This is to test the Intrusion disarm state:
        Requirement ID: https://ford.atlassian.net/browse/ZOPRO-22373
        https://ford.atlassian.net/browse/ZOPRO-26902
        """
        trigger_val = args.inputs

        self.step(CommonStrings.setting_intrusion_armed_str)
        self.set_intrusion_armed_and_activate(trigger=False)

        self.step("set perimeter alarm = Disarmed")
        self.set_disarmed_mode()

        if trigger_val == 'True':
            self.finish_alarm_cycle()

        self.step(CommonStrings.setting_intrusion_triggered_str)
        self.memory.write(CommonStrings.intru_sensor_trig_data_var, SensorTriggeredData.
                          SensorTriggeredDataEnum_TRIGGERED, 'uint8')

        self.call_10ms_runnable_multiple_times(2)

        self.verify_perimeter_alarm_not_activated()

    def test_intrusion_disarm_state_with_extdoorhandlestatus(self, args):
        """
        This is to test the Intrusion disarm state:
        Requirement ID: https://ford.atlassian.net/browse/ZOPRO-22373
        https://ford.atlassian.net/browse/ZOPRO-26902
        """

        trigger_val = args.inputs

        dr_list = [0, 1, 2, 3, 4, 5, 9]
        self.step(CommonStrings.setting_intrusion_armed_str)
        self.set_intrusion_armed_and_activate(trigger=False)

        self.step("set exteriorDoorHandleStatus  = Unlock")
        for drid in dr_list:
            self.memory.write("Rte_PerimeterAlrmVehMdeNewTrgEvnt_exteriorDoorHandleStatus_onChange_"
                              "exteriorDoorHandleStatus[{}]".format(drid),
                              ExteriorDoorHandleStatus.ExteriorDoorHandleStatus_UNLOCKED, 'uint8')

        if trigger_val == 'True':
            self.finish_alarm_cycle()

        self.step(CommonStrings.setting_intrusion_triggered_str)
        self.memory.write(CommonStrings.intru_sensor_trig_data_var, SensorTriggeredData.
                          SensorTriggeredDataEnum_TRIGGERED, 'uint8')

        self.call_10ms_runnable_multiple_times()

        self.verify_perimeter_alarm_not_activated()

    def test_intrusion_disarm_state_with_climateairflowlvl(self, args):
        """
        This is to test the Intrusion disarm state:
        Requirement ID: https://ford.atlassian.net/browse/ZOPRO-22373
        https://ford.atlassian.net/browse/ZOPRO-26902
        """
        (alarmstat, trigger_val) = args.inputs.split("::")
        if alarmstat != "act":
            trig = False
            self.step(CommonStrings.setting_intrusion_armed_str)
        else:
            trig = True
            self.step(CommonStrings.setting_intrusion_triggered_str)
        self.set_intrusion_armed_and_activate(trig)

        self.step("set climate air flow lv  = 1")
        self.memory.write(CommonStrings.climate_airflow_lvl_var, 1, 'uint8')

        if trigger_val == 'True':
            self.finish_alarm_cycle()

        self.step(CommonStrings.setting_intrusion_triggered_str)
        self.memory.write(CommonStrings.intru_sensor_trig_data_var, SensorTriggeredData.
                          SensorTriggeredDataEnum_TRIGGERED, 'uint8')

        self.call_10ms_runnable_multiple_times()

        self.verify_perimeter_alarm_not_activated()

    def test_intrusion_disarm_state_with_doorajarstatus(self, args):
        """
        This is to test the Intrusion disarm state:
        Requirement ID: https://ford.atlassian.net/browse/ZOPRO-22373
        https://ford.atlassian.net/browse/ZOPRO-26902
        """
        doorid = args.inputs
        doorid_val = DrID.from_str(doorid)

        self.step(CommonStrings.setting_prearmed_mode_str)
        self.set_prearmed_mode()

        self.step(CommonStrings.setting_doorajarstatus_str.format(doorid_val, 'AJAR'))
        self.memory.write(CommonStrings.door_ajar_status_variable.format(doorid_val), DrAjarStatus.AJAR, 'uint8')
        self.call_10ms_runnable_multiple_times()

        self.verify_perimeter_alarm_not_activated()

    def test_intru_incli_reset_behavior(self, args):
        """
        This is to test the Intrusion disarm state:
        Requirement ID: https://ford.atlassian.net/browse/ZOPRO-22308
        """
        trigger_name, sensortriggerdata = args.inputs.split("::")
        sensortriggerdata_var = SensorTriggeredData.from_str(sensortriggerdata)
        if trigger_name == "intru":
            self.step(CommonStrings.setting_intrusion_armed_str)
            self.set_intrusion_armed_and_activate(False)
        else:
            self.step(CommonStrings.setting_inclination_armed_str)
            self.set_inclination_armed_and_activate(False)

        self.step(CommonStrings.setting_armed_mode_str)
        self.set_armed_mode()

        if trigger_name == "intru":
            self.step("Set the intrusion sensortriggerdata = {}".format(sensortriggerdata_var))
            self.memory.write(CommonStrings.intru_sensor_trig_data_var, sensortriggerdata_var, 'uint8')
        else:
            self.step("Set the inclination sensortriggerdata = {}".format(sensortriggerdata_var))
            self.memory.write(CommonStrings.incli_sensor_trig_data_var, sensortriggerdata_var, 'uint8')

        self.call_10ms_runnable_multiple_times(2)

        self.step(CommonStrings.checking_alarm_status_str)
        if sensortriggerdata == 'trig':
            self.verify_perimetere_alarm_activated()
        else:
            self.verify_perimetere_alarm_armed()
