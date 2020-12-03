import os
import pytest
import testinfra

import testinfra.utils.ansible_runner

testinfra_hosts = testinfra.utils.ansible_runner.AnsibleRunner(
    os.environ['MOLECULE_INVENTORY_FILE']).get_hosts('rpi')


@pytest.fixture()
def ansible_host(host):
    all_variables = host.ansible.get_variables()
    return all_variables['inventory_hostname']


def test_ssh_force(host):
    f = host.file("/mnt/ssh")
    assert f.exists


def test_removed_known_host_from_localhost(ansible_host):
    localhost = testinfra.get_host("local://")
    localhost.run_expect([1], f"ssh-keygen -F {ansible_host}")
