"""This file contains the main logic behind registering classes for the
fordsim_runner. A test author need not modify/add to this file.
"""
import os
import json
import six
import logging
import vlab
import subprocess

from sos_constants import PostCrashSts, SosPostCrashSts, UseCaseNumber
from software_utils_rh850 import VlabMemory
from software_utils_rh850 import CORE0
from pata_constants import (CommonStrings, PerimeterAlrmStat, PerimeterAlarmCfgM2, LifeCycMdeDActl,
                            VehPwMdeStat, OnChangeInfiniteTimerStatus, ExteriorVehicleLockStatus,
                            LastLockUnlockRequestor, Timer, DrAjarStatus, ReducedGuard, TrailerAlarmActivation,
                            WarningLightRequest, SoundRequest, TrailerConnectCfgM2, TrailerConnection,
                            OnChangeTrailerAlarmSetting, SecurityCfgM2, ExteriorDoorHandleStatus, SensorTriggeredData,
                            SensorState)

_registered_classes = {}
THIS_FILE_DIR = os.path.dirname(os.path.realpath(__file__))

BUILD_TYPE = "Debug"
if os.environ.get('BUILD_TYPE', 'Debug') == "Release":
    BUILD_TYPE = "Release"


def register(cls):
    """Register the class in its global namespace"""
    _registered_classes[cls.__name__] = cls
    return cls


class RegisterMetaClass(type):
    """Metaclass which will do the actual registering"""

    def __new__(cls, clsname, bases, attrs):
        _cls = super(RegisterMetaClass, cls).__new__(cls,
                                                     clsname,
                                                     bases,
                                                     attrs)
        register(_cls)
        return _cls


@six.add_metaclass(RegisterMetaClass)
class VlabTestCase:
    """A Test Case bases which should be inherited by all test scripts in
    suite
    """

    _increment = 0
    output_file = os.environ['coverage_folder']+"/aggregated_coverage.txt"
    counter_log_file = os.environ['coverage_folder'] + '/testcase_ctr.txt'
    coverage_folder = os.environ['coverage_folder']
    annot_file = os.environ['coverage_folder'] + '/annot_dictionary.txt'
    elf_filepaths = os.environ['coverage_folder'] + '/elf_file_names.txt'
    files_to_exclude = ["main", "run_app", "basic_print", "print_buff", "_start_core", "Mfx.*", "Mfl.*", "Ifx.*",
                        "Ifl.*", "Efx.*", "vsnprintf", "snprintf", "___gh_.*", "__ghs.*", "___ghs.*", "__start",
                        "_exit", "_memset", "_sputc_limit", "_strlen", "_strnlen", "_unsout",
                        "_wctomb", "_xdecout", "_xxdecout,memcpy", "___mcopy", "___dotsyscall", "__Exit"]

    def increment_value(self, args):
        if os.path.exists(self.counter_log_file):
            with open(self.counter_log_file, 'r') as f:
                current_value = int(f.read())
        else:
            current_value = 0

        current_value += 1

        with open(self.counter_log_file, 'w') as f:
            f.write(str(current_value))

        return str(current_value)

    def get_elf_file_names(self, args):
        existing_data = ""
        if os.path.exists(self.elf_filepaths):
            with open(self.elf_filepaths, "r") as file:
                existing_data = file.readline().rstrip()
        elf_name = os.path.basename(self.get_elf_filepath(args))
        logging.info("Elf file name: %s", elf_name)
        if elf_name not in existing_data:
            if existing_data != "":
                new_line = ",".join([existing_data, elf_name])
            else:
                new_line = elf_name
            with open(self.elf_filepaths, "w") as file:
                file.write(new_line)

    def get_src_files_mapping(self, args):
        cmd = ['python3']
        cmd += [os.getcwd()+'/fetch_folderpaths_elf.py']
        arguments_for_script_b = [self.get_elf_filepath(args)]
        result = subprocess.check_output(cmd+arguments_for_script_b)
        docker_path = result.split()[0]
        local_path = result.split()[1]
        logging.info("docker path: %s", docker_path)
        logging.info("local path: %s", local_path)

        # Read existing content from the text file
        existing_data = {}
        logging.info("annotation dictionary path: %s", self.annot_file)
        if os.path.isfile(self.annot_file):
            with open(self.annot_file, 'r') as file:
                existing_data = json.load(file)
        else:
            logging.info("annotation dictionary file created")
            existing_data = {}

        # Check if elf_file_path already exists
        if self.get_elf_filepath(args) not in existing_data:
            # Append new data to the dictionary
            existing_data[self.get_elf_filepath(args)] = [(local_path, docker_path)]

            # Write the updated content back to the text file
            with open(self.annot_file, 'w') as file:
                json.dump(existing_data, file, indent=2)

    def before(self, args):
        logging.info("==============================================================================")
        logging.info("FordSIM - RH850G4.U2A")
        logging.info("==============================================================================")

        self.memory = VlabMemory()
        # starts the u2a platform
        vlab.load(
            "rh850g4.u2a",
            args=["--device-type=16"],
        )
        vlab.load_image(self.get_elf_filepath(args), subject=CORE0)

        # Fetch all elf files
        self.get_elf_file_names(args)

        # Fetching docker and local conan folder path mapping dictionary from .elf file
        if int(os.environ['GEN_COVERAGE']) == 1:
            self.get_src_files_mapping(args)

        vlab.enable_analysis(vlab.analysis.view.code_coverage)
        vlab.analysis.scenario.code_coverage(excluded=r','.join(self.files_to_exclude), update=True)
        # Workaround solution: disabled branch and mcdc coverage
        vlab.analysis.scenario.code_coverage(
            function=True, branch=False, mcdc=False, call=False, update=True
        )

        bp = vlab.add_breakpoint(vlab.trigger.execute("run_app"))
        vlab.run(blocking=True)
        vlab.remove_breakpoint(bp)

    def after(self, args):
        # Workaround solution: disabled branch and mcdc coverage
        testcase_ctr = self.increment_value(args)
        logging.info("testcase_ctr: %s", testcase_ctr)
        elf_name = os.path.splitext(os.path.basename(self.get_elf_filepath(args)))[0]
        coverage_file = os.path.join(self.coverage_folder, elf_name + '_' + args.testcase + testcase_ctr + ".xml")
        logging.info("Coverage file %s", coverage_file)
        vlab.analysis.scenario.code_coverage(
            datafile=coverage_file, update=True
        )

        configure_view = vlab.analysis.view.code_coverage(
            datafiles=[coverage_file], output=self.output_file
        )
        vlab.display_analysis(configure_view)

    def get_elf_filepath(self, args):
        if args.elf is None:
            return "/home/dev/build/{}/{}".format(BUILD_TYPE, self.ELF_FILENAME)
        return args.elf

    def verify_equal(self, actual, expected, msg=None):
        """Verify wether the actual value is equal to the expected value. If
        it is not it will raise assertion error.

        :param actual:   The actual value which is obtained from the test case
        :type  actual:   obj
        :param expected: The expected value to be verified against actual.
        :type  expected: obj
        :param msg:      Message to be recorded
        :type  msg:      str, optional
        """
        try:
            assert actual == expected
        except AssertionError:
            _msg = ""
            if msg is not None:
                _msg += "Verify Equal: msg = {}\n".format(msg)
            _msg += "Verify Equal: Assertion FAILED actual='{}'".format(actual)
            _msg += " is not equal to expected='{}'".format(expected)
            raise AssertionError(_msg)
        else:
            if msg is not None:
                logging.info("Verify Equal: msg = {}\n".format(msg))
            _msg = "Verify Equal: Actual = '{}' ".format(actual)
            _msg += "is equal to expected = '{}'".format(expected)
            logging.info(_msg)

    def step(self, msg, step_no=True):
        """Add a step method for better logging.

        :param msg:     Message to be logged
        :type  msg:     str
        :param step_no: Enable or disable the number logging in the step,
                        defaults to True
        :type  step_no: bool, optional
        """
        if step_no:
            self._increment += 1
            s_no = " {}".format(self._increment)
        else:
            s_no = ""
        logging.info("------------------------------------------------------"
                     "---------")
        logging.info("Step {}: {}".format(s_no, msg))
        logging.info("------------------------------------------------------"
                     "---------")

    def call_10ms_runnable_multiple_times(self, no_of_times=1):
        for _ in range(no_of_times):
            vlab.call_software("RePerimeterAlrmVehMdeNewTrgEvnt10mSec", blocking=True)

    def call_10ms_sos_runnable(self, no_of_times=1):
        for _ in range(no_of_times):
            vlab.call_software("SOSPostCrashAlert10ms", blocking=True)

    def set_disarmed_mode(self):
        self.memory.write("Rte_PerimeterAlrmVehMdeNewTrgEvnt_VehPwMdeStat_Grp", VehPwMdeStat.VPM60, 'uint8')
        self.call_10ms_runnable_multiple_times(3)
        self.verify_perimetere_alarm_disarmed()

    def set_prearmed_mode(self):
        self.memory.write("PerimeterAlrmVehMdeNewTrgEvnt_NvmCczmDE10PerimeterAlarmCfgM2",
                          PerimeterAlarmCfgM2.ENABLED, 'Boolean')
        self.memory.write("Rte_PerimeterAlrmVehMdeNewTrgEvnt_LifeCycleMode_Val", LifeCycMdeDActl.NORMAL, 'uint8')
        self.memory.write("Rte_PerimeterAlrmVehMdeNewTrgEvnt_VehPwMdeStat_Grp", VehPwMdeStat.VPM40, 'uint8')
        self.memory.write("Rte_PerimeterAlrmVehMdeNewTrgEvnt_onChange_infiniteTimerStatusInterface_"
                          "onChange_infiniteTimerStatus", OnChangeInfiniteTimerStatus.RequestStatusType_DEFAULT,
                          'uint8')
        self.memory.write("Rte_PerimeterAlrmVehMdeNewTrgEvnt_exteriorVehicleLockStatus_"
                          "onChange_exteriorVehicleLockStatus", ExteriorVehicleLockStatus.CENTRALLY_LOCKED, 'uint8')
        self.memory.write("Rte_PerimeterAlrmVehMdeNewTrgEvnt_lastLockUnlockRequestor_onChange_lastLockUnlockRequestor",
                          LastLockUnlockRequestor.REMOTE, 'uint8')
        self.memory.write("Rte_PerimeterAlrmVehMdeNewTrgEvnt_exteriorLockEventCount_onChange_exteriorLockEventCount",
                          1, 'uint8')
        self.call_10ms_runnable_multiple_times(3)

        self.step("verifying the alarm state == PREARMED")
        self.verify_perimetere_alarm_prearmed()

    def set_armed_mode(self):
        perimeter_alarm_state = self.memory.read("Rte_PerimeterAlrmVehMdeNewTrgEvnt_PerimeterAlrmStat_Val", 'uint8')
        if perimeter_alarm_state != PerimeterAlrmStat.PerimeterAlrmStat_ARMED:
            if perimeter_alarm_state != PerimeterAlrmStat.PerimeterAlrmStat_PREARMED:
                self.set_prearmed_mode()
            tmr_sec_cnt = Timer.INITIAL_TIMER
            while tmr_sec_cnt < Timer.ARMING_DELAY_TIMER:
                self.memory.write("Rte_PerimeterAlrmVehMdeNewTrgEvnt_TmrSecCnt_DeVal", tmr_sec_cnt, "uint32")
                self.call_10ms_runnable_multiple_times()
                self.verify_perimetere_alarm_prearmed()
                tmr_sec_cnt += 10
            self.memory.write("Rte_PerimeterAlrmVehMdeNewTrgEvnt_TmrSecCnt_DeVal", tmr_sec_cnt, "uint32")
            self.call_10ms_runnable_multiple_times()

            self.step("At/After Arming delay timer == 20 sec Alarm status should be ARMED")
            self.verify_perimetere_alarm_armed()
        self.verify_perimetere_alarm_armed()

    def set_activated_mode(self):
        perimeter_alarm_state = self.memory.read("Rte_PerimeterAlrmVehMdeNewTrgEvnt_PerimeterAlrmStat_Val", 'uint8')

        if perimeter_alarm_state != PerimeterAlrmStat.PerimeterAlrmStat_ARMED:
            self.step(CommonStrings.setting_armed_mode_str)
            self.set_armed_mode()

        self.step("Set doorAjarStatus[0] = AJAR")
        self.memory.write("Rte_PerimeterAlrmVehMdeNewTrgEvnt_doorAjarStatus_onChange_doorAjarStatus[0]",
                          DrAjarStatus.AJAR, 'uint8')
        self.call_10ms_runnable_multiple_times(3)
        self.verify_perimetere_alarm_activated()

    def set_reduced_guard_on(self):
        self.set_prearmed_mode()

        self.memory.write("Rte_PerimeterAlrmVehMdeNewTrgEvnt_ReducedGuardDRq_Val",
                          ReducedGuard.ReducedGuard_ON, 'uint8')
        self.call_10ms_runnable_multiple_times()
        result = self.memory.read("Rte_PerimeterAlrmVehMdeNewTrgEvnt_ReducedGuardDStat_Val", 'uint8')
        self.verify_equal(result, ReducedGuard.ReducedGuard_ON)

    def verify_perimetere_alarm_disarmed(self):
        alarmstatus = self.memory.read("Rte_PerimeterAlrmVehMdeNewTrgEvnt_PerimeterAlrmStat_Val", "uint8")
        self.verify_equal(alarmstatus, PerimeterAlrmStat.PerimeterAlrmStat_DISARMED)

    def verify_perimetere_alarm_prearmed(self):
        alarmstatus = self.memory.read("Rte_PerimeterAlrmVehMdeNewTrgEvnt_PerimeterAlrmStat_Val", "uint8")
        self.verify_equal(alarmstatus, PerimeterAlrmStat.PerimeterAlrmStat_PREARMED)

    def verify_perimetere_alarm_armed(self):
        alarmstatus = self.memory.read("Rte_PerimeterAlrmVehMdeNewTrgEvnt_PerimeterAlrmStat_Val", "uint8")
        self.verify_equal(alarmstatus, PerimeterAlrmStat.PerimeterAlrmStat_ARMED)

    def verify_perimetere_alarm_activated(self):
        alarmstatus = self.memory.read("Rte_PerimeterAlrmVehMdeNewTrgEvnt_PerimeterAlrmStat_Val", "uint8")
        self.verify_equal(alarmstatus, PerimeterAlrmStat.PerimeterAlrmStat_ACTIVATED)

    def verify_perimeter_alarm_not_activated(self):
        self.step("Verify alarm should not be activated")
        alarmstatus = self.memory.read("Rte_PerimeterAlrmVehMdeNewTrgEvnt_PerimeterAlrmStat_Val", "uint8")
        if alarmstatus != PerimeterAlrmStat.PerimeterAlrmStat_ACTIVATED:
            alarmstatus = "Not Activated"
        self.verify_equal(alarmstatus, "Not Activated")

    def inhibit_state_verfication(self, doorid_val):
        self.step("Set doorAjarStatus[{}] = AJAR".format(doorid_val))
        self.memory.write(CommonStrings.door_ajar_status_variable.format(doorid_val), DrAjarStatus.AJAR, 'uint8')
        self.call_10ms_runnable_multiple_times(3)
        self.verify_perimetere_alarm_activated()

    def check_alarm(self, alarmstatus):
        self.step(CommonStrings.checking_alarm_status_str)
        if alarmstatus == 'prearm':
            self.verify_perimetere_alarm_prearmed()
        elif alarmstatus == 'disarm':
            self.verify_perimetere_alarm_disarmed()
        elif alarmstatus == 'arm':
            self.verify_perimetere_alarm_armed()
        else:
            self.verify_perimetere_alarm_activated()

    def verify_trailer_alarm(self):
        trailer_alarm_stat = self.memory.read("Rte_PerimeterAlrmVehMdeNewTrgEvnt_onChange_"
                                              "trailerAlarmInterface_onChange_trailerAlarm", "uint8")
        self.step(CommonStrings.checking_trailer_alarm_str)
        self.verify_equal(trailer_alarm_stat, TrailerAlarmActivation.TrailerAlarmActivation_TRAILER_ALARM_ACTIVE)

    def verify_warning_light_on_off(self, value):
        warning_light_request_stat = self.memory.read("PerimeterAlrmVehMdeNewTrgEvnt_TurnLghtSrvcIntfc_"
                                                      "SomeIpmflashWarningLight_WarningLightRequest", 'uint8')
        if value == "off":
            self.verify_equal(warning_light_request_stat, WarningLightRequest.OFF)
        else:
            self.verify_equal(warning_light_request_stat, WarningLightRequest.ON)

    def verify_sound_request(self, value):
        soundrequest_stat = self.memory.read("PerimeterAlrmVehMdeNewTrgEvnt_SounderServiceInterface_"
                                             "actuateSounder_soundRequest", 'uint8')
        if value == "deactivate":
            self.verify_equal(soundrequest_stat, SoundRequest.DEACTIVATE)
        else:
            self.verify_equal(soundrequest_stat, SoundRequest.ACTIVATE)

    def set_trailer_alarm_armed(self):
        self.step("Arming trailer Alarm")
        self.memory.write("PerimeterAlrmVehMdeNewTrgEvnt_NvmCczmPATrailerConnectCfgM2", TrailerConnectCfgM2.ENABLED,
                          'Boolean')
        self.memory.write(
            "Rte_PerimeterAlrmVehMdeNewTrgEvnt_onChange_trailerConnectionInterface_onChange_trailerConnection",
            TrailerConnection.TrailerConnection_TRAILER_CONNECTION_YES, 'uint8')
        self.call_10ms_runnable_multiple_times()
        self.set_prearmed_mode()
        self.set_armed_mode()
        self.memory.write("Rte_PerimeterAlrmVehMdeNewTrgEvnt_onChange_trailerAlarmSetting_onChange_trailerAlarmSetting",
                          OnChangeTrailerAlarmSetting.TrailerConnectionAlarmSetting_ON, 'uint8')
        self.call_10ms_runnable_multiple_times()
        self.verify_trailer_alarm()

    def finish_alarm_cycle(self):
        self.step("waiting for 285 sec to fininsh alarm cycle")
        self.memory.write("Rte_PerimeterAlrmVehMdeNewTrgEvnt_TmrSecCnt_DeVal", 305, "uint32")
        self.call_10ms_runnable_multiple_times()

    def dont_finish_alarm_cycle(self):
        self.step("waiting for 100 sec after alarm starts")
        self.memory.write("Rte_PerimeterAlrmVehMdeNewTrgEvnt_TmrSecCnt_DeVal", 120, "uint32")
        self.call_10ms_runnable_multiple_times()

    def finish_audible_alarm_time(self):
        self.step("waiting for 30 sec to fininsh alarm cycle")
        self.memory.write("Rte_PerimeterAlrmVehMdeNewTrgEvnt_TmrSecCnt_DeVal", 50, "uint32")
        self.call_10ms_runnable_multiple_times()

    def dont_finish_audible_alarm_time(self):
        self.step("waiting for 10 sec after alarm actiation")
        self.memory.write("Rte_PerimeterAlrmVehMdeNewTrgEvnt_TmrSecCnt_DeVal", 30, "uint32")
        self.call_10ms_runnable_multiple_times()

    def set_intrusion_armed_and_activate(self, trigger=True):
        """
        sets the intrusion sensing to arm or activate based on the values passed.
        :param trigger: Default it is True, In case of True it will activate the intrusion alarm
                        and in case of False it will not activate the alarm
        :type  trigger:Boolean
        """
        dr_list = [0, 1, 2, 3, 4, 5, 9]
        # driver door, passenger door, driver second row, passenger second row, bec, bec2, bec3
        self.memory.write("PerimeterAlrmVehMdeNewTrgEvnt_NvmCczmDE10SecurityCfgM2",
                          SecurityCfgM2.SECURITYCFG_INTRUSION, 'uint8')

        self.set_prearmed_mode()

        self.memory.write("Rte_PerimeterAlrmVehMdeNewTrgEvnt_ReducedGuardDRq_Val",
                          ReducedGuard.ReducedGuard_NULL, 'uint8')

        for drid in dr_list:
            self.memory.write(CommonStrings.ext_door_handle_variable.format(drid),
                              ExteriorDoorHandleStatus.ExteriorDoorHandleStatus_LOCKED, 'uint8')

            self.memory.write(CommonStrings.door_ajar_status_variable.format(drid), DrAjarStatus.CLOSED, 'uint8')

        self.memory.write(CommonStrings.climate_airflow_lvl_var, 0, 'uint8')

        if trigger is not True:
            self.memory.write(CommonStrings.intru_sensor_trig_data_var,
                              SensorTriggeredData.SensorTriggeredDataEnum_NOT_TRIGGERED, 'uint8')
        self.set_armed_mode()

        self.memory.write(CommonStrings.intru_sensor_state_var, SensorState.SensorStateEnum_ARMED, 'uint8')

        self.call_10ms_runnable_multiple_times(2)

    def set_inclination_armed_and_activate(self, trigger=True):
        """
        sets the Inclination sensing to arm or activate based on the values passed.
        :param trigger: Default it is True, In case of True it will activate the intrusion alarm
                        and in case of False it will not activate the alarm
        :type  trigger:Boolean
        """
        dr_list = [0, 1, 2, 3, 4, 5, 9]
        # driver door, passenger door, driver second row, passenger second row, bec, bec2, bec3
        self.memory.write("PerimeterAlrmVehMdeNewTrgEvnt_NvmCczmDE10SecurityCfgM2",
                          SecurityCfgM2.SECURITYCFG_INCLINATION, 'uint8')

        self.set_prearmed_mode()

        self.memory.write("Rte_PerimeterAlrmVehMdeNewTrgEvnt_ReducedGuardDRq_Val",
                          ReducedGuard.ReducedGuard_NULL, 'uint8')

        for drid in dr_list:
            self.memory.write(CommonStrings.ext_door_handle_variable.format(drid),
                              ExteriorDoorHandleStatus.ExteriorDoorHandleStatus_LOCKED, 'uint8')

            self.memory.write(CommonStrings.door_ajar_status_variable.format(drid), DrAjarStatus.CLOSED, 'uint8')

        if trigger is not True:
            self.memory.write(CommonStrings.incli_sensor_trig_data_var,
                              SensorTriggeredData.SensorTriggeredDataEnum_NOT_TRIGGERED, 'uint8')
        self.set_armed_mode()

        self.memory.write(CommonStrings.incli_sensor_state_var, SensorState.SensorStateEnum_ARMED, 'uint8')

        self.call_10ms_runnable_multiple_times(2)

    def verify_crash_event_occurrence(self, pos_crash_sts_value, sos_pos_crash_sts_value, usecase_value,
                                      crash_event=True):

        if crash_event:
            self.step("Verify PostCrashSts value")
            self.verify_equal(pos_crash_sts_value, PostCrashSts.TRUE)

            self.step("Verify SOSPostCrashSts value")
            self.verify_equal(sos_pos_crash_sts_value, SosPostCrashSts.TRUE)

            self.step("Verify Usecasid value in ResourceManagerDirect_startUseCase")
            self.verify_equal(usecase_value, UseCaseNumber.CRASH_EVENT_OCCURRENCE)

        else:
            self.step("Verify PostCrashSts value")
            self.verify_equal(pos_crash_sts_value, PostCrashSts.FALSE)

            self.step("Verify SOSPostCrashSts value")
            self.verify_equal(sos_pos_crash_sts_value, SosPostCrashSts.FALSE)

            self.step("Verify Usecasid value in ResourceManagerDirect_startUseCase")
            if usecase_value != UseCaseNumber.CRASH_EVENT_OCCURRENCE:
                usecase_value = True
            self.verify_equal(usecase_value, True)
