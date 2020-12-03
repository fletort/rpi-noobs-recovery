import os
import pytest

import testinfra.utils.ansible_runner

testinfra_hosts = testinfra.utils.ansible_runner.AnsibleRunner(
    os.environ['MOLECULE_INVENTORY_FILE']).get_hosts('rpi')


@pytest.mark.parametrize('option', [
  'silentinstall',
  'runinstaller'
])
def test_cmdline_options(host, option):
    f = host.file("/mnt/recovery.cmdline")
    assert f.contains(option)
