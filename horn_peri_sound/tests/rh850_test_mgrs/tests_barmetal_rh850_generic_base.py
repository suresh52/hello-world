import os
import slash
import subprocess
from pathlib import Path


VLAB_SCRIPT_FOLDER = (Path(__file__).parent / "../../rh850").resolve()
VLAB_SCRIPT_RUNNER = str(VLAB_SCRIPT_FOLDER) + "/_fordsim_runner.py"


class Rh850Base(slash.Test):
    """Rh850Base
    Common functions for EAP TLS
    """
    logger = slash.logger
    custom_elf_cmd = []

    def before(self):
        """Rh850Base - Before test execution"""

        # Check if the environment variable "CUSTOM_RH850_ELF" exists, if it does then this means this is called by the
        # CI/CD environment with a custom ELF file.
        if "CUSTOM_RH850_ELF" in os.environ:
            self.custom_elf_cmd = ["--elf", os.environ["CUSTOM_RH850_ELF"]]
            self.logger.info("Using Custom ELF file.")
        else:
            self.logger.info("Using Default ELF file set by the scripts.")

        self.logger.debug("Rh850Base.before()")

    def after(self):
        """Rh850Base - After test execution"""
        self.logger.debug("Rh850Base.after()")

    def execute_vlab_test(self, tc_name_or_id: str, inputs: str = None,
                          outputs: str = None) -> subprocess.CompletedProcess:
        """Generic function which will execute the test by searching in the folder.

        :param tc_name_or_id: TC name or ID to be executed
        :type  tc_name_or_id: str
        :param inputs:        Optional, Input to be passed to the test.
                              .. note:: This will be passed as string to the TC
        :type  inputs:        str
        :param outputs:       Optional, Expected output to be passed to the test case.
                              .. note:: This will be passed as a string to the TC
        :type  outputs:       str
        :return:              Return the Subprocess completed object
        :rtype:               CompletedProcess
        """
        if os.environ.get('BUILD_TYPE', 'Debug').lower() == "debug-ide":
            cmd = ['vlab-ide']
        else:
            cmd = ['vlab']

        cmd += [VLAB_SCRIPT_RUNNER, "--testcase", tc_name_or_id] + self.custom_elf_cmd
        if inputs is not None:
            cmd.extend(['--inputs', inputs])
        if outputs is not None:
            cmd.extend(['--outputs', outputs])

        # Execute the command and capture the output and return code
        self.logger.info("Executing TC '{}' through vlab command".format(tc_name_or_id))
        self.logger.info(" ".join(cmd))
        result = subprocess.run(cmd, check=False, cwd=VLAB_SCRIPT_FOLDER)
        return result

    def _assert_return_code(self, result):
        log_file = slash.config.root.log.subpath.format(context=slash.context)
        assert_str = "Failures occurred during test execution check the " \
                     f"following log file for details:\n{log_file}"
        assert result.returncode == 0, assert_str
