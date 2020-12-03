import os
import pytest
import testinfra

import testinfra.utils.ansible_runner

testinfra_hosts = testinfra.utils.ansible_runner.AnsibleRunner(
    os.environ['MOLECULE_INVENTORY_FILE']).get_hosts('client_ssh')


@pytest.fixture()
def rpi_hostnames():
    all_rpi = testinfra.utils.ansible_runner.AnsibleRunner(
        os.environ['MOLECULE_INVENTORY_FILE']).get_hosts('client_ssh')
    return all_rpi


def test_removed_known_host(host, rpi_hostnames):
    for rpi_host in rpi_hostnames:
        host.run_expect([1], f"ssh-keygen -F {rpi_host}")


