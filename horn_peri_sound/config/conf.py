# In this file, the default configuration for the test repo is defined.
# Everything in conf.py will be applied to slash and will be available to all
# tests as the default configuration. It is usual to overwrite some or all of
# this default configuration information with local configuration information.

from copy import deepcopy

# Python's confetti framework which deals with hierarchical configuration data
# is used to create the configuration.
from confetti import Config

# Import library resource configurations
from testbed_test_lib.basic_configs import (
    windows_config,
    ubuntu_vm_config,
    eb_linux_config,
    wr_linux_config,
    qnx_config,
    qemu_config,
    service_config,
    env_configuration
)

# Limit Python to only use the "config" variable from this module
__all__ = ["config"]
config = env_configuration.get("config", {})

# Instantiate and customize, as required, the imported resource configs
#   Note: The FATHER_KEY attribute must be defined for each imported
#         configuration. This attribute defines the "root" point in the
#         config hierarchy for the resource, so the value of this attribute
#         for each resource needs to be unique.
FATHER_KEY = "father_key"
WINDOWS_KEY = "Windows"
UBUNTU_VM_KEY = "UbuntuVM"

EBLINUX_KEY = "EbLinux"
EB_QEMU_KEY = "EbQemu"
EB_SERVICE_KEY = "EbExampleService"
EB_PYBIND_KEY = "EbPythonBinding"
EB_TP_SERVICE_KEY = "EB_ExampleService"

WRLINUX_KEY = "WrLinux"
WR_QEMU_KEY = "WrQemu"
WR_SERVICE_KEY = "WrExampleService"
WR_PYBIND_KEY = "WrPythonBinding"

QNX_KEY = "Qnx"
QNX_QEMU_KEY = "QnxQemu"
QNX_SERVICE_KEY = "QnxExampleService"
QNX_PYBIND_KEY = "QnxPythonBinding"

EB_SVC1_GROUP = "EB_SVC1"
EB_SVC2_GROUP = "EB_SVC2"
QNX_WR_GROUP = "QNX_WR"

config[WINDOWS_KEY] = windows_config

ubuntu_vm_config[FATHER_KEY] = WINDOWS_KEY
config[UBUNTU_VM_KEY] = ubuntu_vm_config

# EB Linux resources
eb_linux_config[FATHER_KEY] = UBUNTU_VM_KEY
config[EBLINUX_KEY] = eb_linux_config

# QEMU (EBLINUX)
eb_qemu = deepcopy(qemu_config)
eb_qemu[FATHER_KEY] = EBLINUX_KEY
config[EB_QEMU_KEY] = eb_qemu

eb_svc_config = deepcopy(service_config)
eb_svc_config["startup_groups"] = EB_SVC1_GROUP
eb_svc_config[FATHER_KEY] = EB_QEMU_KEY
eb_svc_config["node_id"] = "example_service"
config[EB_SERVICE_KEY] = eb_svc_config

# PYBINDING (EBLINUX)
eb_pybind_config = deepcopy(service_config)
eb_pybind_config[FATHER_KEY] = EB_QEMU_KEY
eb_pybind_config["node_id"] = "PythonBinding"
eb_pybind_config["startup_groups"] = f"{EB_SVC1_GROUP}, {EB_SVC2_GROUP}"
config[EB_PYBIND_KEY] = eb_pybind_config

# WR Linux components
wr_linux_config[FATHER_KEY] = UBUNTU_VM_KEY
config[WRLINUX_KEY] = wr_linux_config

# QEMU (WRLINUX)
wr_qemu = deepcopy(qemu_config)
wr_qemu["startup_groups"] = QNX_WR_GROUP
wr_qemu[FATHER_KEY] = WRLINUX_KEY
config[WR_QEMU_KEY] = wr_qemu

wr_svc_config = deepcopy(service_config)
wr_svc_config[FATHER_KEY] = WR_QEMU_KEY
wr_svc_config["node_id"] = "example_service"
wr_svc_config["is_started"] = True
config[WR_SERVICE_KEY] = wr_svc_config

wr_pybind_config = deepcopy(service_config)
wr_pybind_config[FATHER_KEY] = WR_QEMU_KEY
wr_pybind_config["node_id"] = "PythonBinding"
config[WR_PYBIND_KEY] = wr_pybind_config

# QNX components
qnx_config[FATHER_KEY] = UBUNTU_VM_KEY
config[QNX_KEY] = qnx_config

qnx_qemu = deepcopy(qemu_config)
qnx_qemu[FATHER_KEY] = QNX_KEY
qnx_qemu["node_id"] = 3
qnx_qemu["hostname"] = "10.1.0.3"
config[QNX_KEY] = qnx_config

qnx_svc_config = deepcopy(service_config)
qnx_svc_config[FATHER_KEY] = QNX_QEMU_KEY
qnx_svc_config["node_id"] = "example_service"
config[QNX_SERVICE_KEY] = qnx_svc_config

qnx_pybind_config = deepcopy(service_config)
qnx_pybind_config[FATHER_KEY] = QNX_QEMU_KEY
qnx_pybind_config["node_id"] = "PythonBinding"
qnx_pybind_config["startup_groups"] = QNX_WR_GROUP
config[QNX_PYBIND_KEY] = qnx_pybind_config

# Create a Config object to contain the default values for the configuration.
#   This object must be assigned to a variable named "config".
config = Config(env_configuration)
