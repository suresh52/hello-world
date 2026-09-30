import vlab

from common import VlabTestCase
from pata_constants import (CommonStrings, HornSoundCfgM2, SounderPattern, SoundRequest, REPETITION,
                            PauseBetweenRepetition, ActivationTimeStamp, AlarmSoundCfgM2)


class VisualAudibleAlarm(VlabTestCase):
    """
    This class holds the test case for PATA - Visual Audible Alarm.
    """
    # Default elf file to use when it is not provided from slash or CI/CD
    ELF_FILENAME = "PerimeterAlrmVehMdeNewTrgEvnt.elf"

    def before(self, args):
        super(VisualAudibleAlarm, self).before(args)
        self.initialize()

    def after(self, args):
        super(VisualAudibleAlarm, self).after(args)

        vlab.exit()

    def initialize(self):

        self.step("Calling Init function")
        vlab.call_software("RePerimeterAlrmVehMdeNewTrgEvntInit", blocking=True)

    def test_alarmcycle_completion(self, args):
        """
        This is to test the alarmcycle completion:
        Requirement ID: https://ford.atlassian.net/browse/ZOPRO-11357
        """

        timer = args.inputs

        self.memory.write("PerimeterAlrmVehMdeNewTrgEvnt_NvmCczmDE10HornSoundCfgM2", HornSoundCfgM2.ON, "boolean")
        self.call_10ms_runnable_multiple_times()
        self.step(CommonStrings.setting_activated_mode_str)
        self.set_activated_mode()
        self.call_10ms_runnable_multiple_times()
        self.step(CommonStrings.verify_soundrequest_str)
        self.verify_sound_request('activate')

        if timer == "50":
            self.finish_audible_alarm_time()
            self.call_10ms_runnable_multiple_times()
            self.step(CommonStrings.verify_soundrequest_str)
            self.verify_sound_request('deactivate')
        else:
            self.dont_finish_audible_alarm_time()
            self.call_10ms_runnable_multiple_times()
            self.step(CommonStrings.verify_soundrequest_str)
            self.verify_sound_request('activate')

    def test_alarm_cycle_completion_audible_sound(self, args):
        """
        This is to test the alarmcycle completion:
        Requirement ID: https://ford.atlassian.net/browse/ZOPRO-11357
        """

        alarmstat = args.inputs

        self.memory.write("PerimeterAlrmVehMdeNewTrgEvnt_NvmCczmDE10HornSoundCfgM2", HornSoundCfgM2.ON, "boolean")
        self.call_10ms_runnable_multiple_times()
        if alarmstat != "act":
            if alarmstat == "prearm":
                self.step(CommonStrings.setting_prearmed_mode_str)
                self.set_prearmed_mode()
            if alarmstat == "arm":
                self.step(CommonStrings.setting_armed_mode_str)
                self.set_armed_mode()
            self.step(CommonStrings.verify_soundrequest_str)
            self.verify_sound_request('deactivate')

    def test_alarmcycle_defination(self, args):
        """
        This is to test the alarmcycle defination:
        Requirement ID: https://ford.atlassian.net/browse/ZOPRO-11356
        """

        alarmstat = args.inputs

        self.memory.write("PerimeterAlrmVehMdeNewTrgEvnt_NvmCczmDE10HornSoundCfgM2", HornSoundCfgM2.ON, "boolean")
        self.call_10ms_runnable_multiple_times()
        self.step(CommonStrings.verify_soundrequest_str)
        self.verify_sound_request('deactivate')

        self.step(CommonStrings.verify_warninglightrequest_str)
        self.verify_warning_light_on_off('off')

        if alarmstat != "act":
            if alarmstat == "prearm":
                self.step(CommonStrings.setting_prearmed_mode_str)
                self.set_prearmed_mode()
            if alarmstat == "arm":
                self.step(CommonStrings.setting_armed_mode_str)
                self.set_armed_mode()
            self.step(CommonStrings.verify_soundrequest_str)
            self.verify_sound_request('deactivate')
            self.step(CommonStrings.verify_warninglightrequest_str)
            self.verify_warning_light_on_off('off')

        else:
            self.step(CommonStrings.setting_activated_mode_str)
            self.set_activated_mode()
            self.call_10ms_runnable_multiple_times(3)

            self.step(CommonStrings.verify_soundrequest_str)
            self.verify_sound_request('activate')

            self.step(CommonStrings.verify_warninglightrequest_str)
            self.verify_warning_light_on_off('on')

            self.finish_audible_alarm_time()
            self.call_10ms_runnable_multiple_times()

            self.step(CommonStrings.verify_soundrequest_str)
            self.verify_sound_request('deactivate')

            self.finish_alarm_cycle()
            self.call_10ms_runnable_multiple_times()

            self.step(CommonStrings.verify_warninglightrequest_str)
            self.verify_warning_light_on_off('off')

    def test_audible_alarm_m2_config(self, args):
        """
        This is to test the Audible Alarm M2 config:
        Requirement ID: https://ford.atlassian.net/browse/ZOPRO-11339
        """
        alarmstat = args.inputs

        self.step("set HornSoundCfgM2 = OFF")
        self.memory.write("PerimeterAlrmVehMdeNewTrgEvnt_NvmCczmDE10HornSoundCfgM2", HornSoundCfgM2.OFF, "boolean")
        self.call_10ms_runnable_multiple_times()

        if alarmstat == "prearm":
            self.step(CommonStrings.setting_prearmed_mode_str)
            self.set_prearmed_mode()
        if alarmstat == "arm":
            self.step(CommonStrings.setting_armed_mode_str)
            self.set_armed_mode()
        if alarmstat == "act":
            self.step(CommonStrings.setting_activated_mode_str)
            self.set_activated_mode()

        sound_pattern_val = self.memory.read("PerimeterAlrmVehMdeNewTrgEvnt_SounderServiceInterface_"
                                             "actuateSounder_soundPattern", "uint8")
        sound_request_val = self.memory.read("PerimeterAlrmVehMdeNewTrgEvnt_SounderServiceInterface_"
                                             "actuateSounder_soundRequest", "uint8")
        repetition_val = self.memory.read("PerimeterAlrmVehMdeNewTrgEvnt_SounderServiceInterface_"
                                          "actuateSounder_repetitions", "uint16")
        pause_between_repetition_val = self.memory.read("PerimeterAlrmVehMdeNewTrgEvnt_SounderServiceInterface_"
                                                        "actuateSounder_pauseBetweenRepetition", "uint16")
        activation_times_tamp_val = self.memory.read("PerimeterAlrmVehMdeNewTrgEvnt_SounderServiceInterface_"
                                                     "actuateSounder_activationTimeStamp", "uint32")

        self.verify_equal(sound_pattern_val, SounderPattern.CHIRP_1)
        self.verify_equal(sound_request_val, SoundRequest.DEACTIVATE)
        self.verify_equal(repetition_val, REPETITION.DEFAULT_VALUE)
        self.verify_equal(pause_between_repetition_val, PauseBetweenRepetition.DEFAULT_VALUE)
        self.verify_equal(activation_times_tamp_val, ActivationTimeStamp.DEFAULT_VALUE)

    def test_visual_outputs(self, args):
        """
        This is to test the Visual Outputs:
        Requirement ID: https://ford.atlassian.net/browse/ZOPRO-11361
        """

        alarmstat = args.inputs

        if alarmstat != "act":
            if alarmstat == "prearm":
                self.step(CommonStrings.setting_prearmed_mode_str)
                self.set_prearmed_mode()
            if alarmstat == "arm":
                self.step(CommonStrings.setting_armed_mode_str)
                self.set_armed_mode()
            self.step(CommonStrings.verify_warninglightrequest_str)
            self.verify_warning_light_on_off('off')

        if alarmstat == "act":
            self.step(CommonStrings.setting_activated_mode_str)
            self.set_activated_mode()
            self.step(CommonStrings.verify_warninglightrequest_str)
            self.verify_warning_light_on_off('on')

    def test_visual_outputs_after_alarmcycle(self, args):
        """
        This is to test the Visual Outputs:
        Requirement ID: https://ford.atlassian.net/browse/ZOPRO-11361
                        https://ford.atlassian.net/browse/ZOPRO-11357
        """

        timer = args.inputs

        self.step(CommonStrings.setting_activated_mode_str)
        self.set_activated_mode()

        self.step(CommonStrings.verify_warninglightrequest_str)
        self.step(CommonStrings.verify_warninglightrequest_str)
        self.verify_warning_light_on_off('on')

        if timer == "305":
            self.finish_alarm_cycle()
            self.call_10ms_runnable_multiple_times()
            self.step(CommonStrings.verify_warninglightrequest_str)
            self.verify_warning_light_on_off('off')
        else:
            self.dont_finish_alarm_cycle()
            self.call_10ms_runnable_multiple_times()
            self.step(CommonStrings.verify_warninglightrequest_str)
            self.verify_warning_light_on_off('on')

    def test_audible_alarm_output_m2_config(self, args):
        """
        This is to test the Audible Alarm Output M2 config:
        Requirement ID: https://ford.atlassian.net/browse/ZOPRO-22340
        """
        (alarmsoundcfg, alarmstat) = args.inputs.split("::")
        alarmsoundcfg_val = AlarmSoundCfgM2.from_str(alarmsoundcfg)
        self.step("set HornSoundCfgM2 = ON")
        self.memory.write("PerimeterAlrmVehMdeNewTrgEvnt_NvmCczmDE10HornSoundCfgM2", HornSoundCfgM2.ON, "boolean")
        self.step("set the AlarmSoundCfgM2")
        self.memory.write("PerimeterAlrmVehMdeNewTrgEvnt_NvmCczmDE10AlarmSoundCfgM2", alarmsoundcfg_val, "uint8")
        self.call_10ms_runnable_multiple_times(3)

        if alarmstat == "prearm":
            self.set_prearmed_mode()
            self.call_10ms_runnable_multiple_times(2)
            sound_pattern_val = self.memory.read("PerimeterAlrmVehMdeNewTrgEvnt_SounderServiceInterface_"
                                                 "actuateSounder_soundPattern", "uint8")
            self.verify_equal(sound_pattern_val, SounderPattern.PERIMETER_ARMBBS)

        elif alarmstat == "arm":
            self.set_armed_mode()
            self.call_10ms_runnable_multiple_times()
            sound_pattern_val = self.memory.read("PerimeterAlrmVehMdeNewTrgEvnt_SounderServiceInterface_"
                                                 "actuateSounder_soundPattern", "uint8")
            self.verify_equal(sound_pattern_val, SounderPattern.PERIMETER_ARMBBS)

        elif alarmstat == "act":
            self.set_activated_mode()
            self.call_10ms_runnable_multiple_times()
            sound_pattern_val = self.memory.read("PerimeterAlrmVehMdeNewTrgEvnt_SounderServiceInterface_"
                                                 "actuateSounder_soundPattern", "uint8")
            if alarmsoundcfg == "bbs":
                self.verify_equal(sound_pattern_val, SounderPattern.PERIMETER_ALARM1_BBS)
            elif alarmsoundcfg == "bbs_vehicle_horn":
                self.verify_equal(sound_pattern_val, SounderPattern.PERIMETER_ALARM2_H_BBS)
            else:
                self.verify_equal(sound_pattern_val, SounderPattern.PERIMETER_ALARM2_H)

        else:
            self.set_disarmed_mode()
            self.call_10ms_runnable_multiple_times()
            sound_pattern_val = self.memory.read("PerimeterAlrmVehMdeNewTrgEvnt_SounderServiceInterface_"
                                                 "actuateSounder_soundPattern", "uint8")
            self.verify_equal(sound_pattern_val, SounderPattern.CHIRP_1)
