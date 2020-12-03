import os
import json
import pytest

import testinfra.utils.ansible_runner

testinfra_hosts = testinfra.utils.ansible_runner.AnsibleRunner(
    os.environ['MOLECULE_INVENTORY_FILE']).get_hosts('rpi')


@pytest.fixture()
def waited_os_dir(host):
    all_variables = host.ansible.get_variables()
    return all_variables['waited_os_dir']


@pytest.fixture()
def waited_os_date(host):
    all_variables = host.ansible.get_variables()
    return all_variables['waited_os_date']


# Listdir
# default listdir can not be used on alpine os as 'q' option of ls command
# is not available on this os by default.
def listdir(host, path):
    reply = []
    cmd = host.run("ls -1 " + path)
    if cmd.succeeded:
        reply = cmd.stdout.splitlines()
    return reply


def test_os_removed(host, waited_os_dir):
    os_list = listdir(host, "/mnt/os")
    assert len(os_list) == 1
    assert os_list[0] == waited_os_dir


def test_os_date(host, waited_os_dir, waited_os_date):
    f = host.file("/mnt/os/"+waited_os_dir+"/os.json")
    assert f.exists
    descriptor = json.loads(f.content_string)
    assert descriptor["release_date"] == waited_os_date
