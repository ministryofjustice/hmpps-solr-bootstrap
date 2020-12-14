import os
import pytest

import testinfra.utils.ansible_runner

testinfra_hosts = testinfra.utils.ansible_runner.AnsibleRunner(
    os.environ['MOLECULE_INVENTORY_FILE']
).get_hosts('all')

solr_base_dir = "/opt/solr/alfresco-search-services"
solr_rerank_conf_dir = f"{solr_base_dir}/data/solrhome/templates/rerank/conf"


def test_mountpoint_present(host):

    mount_point = f"{solr_base_dir}/data"
    assert host.mount_point(mount_point).exists
    assert host.mount_point(mount_point).filesystem == "xfs"


@pytest.mark.parametrize("pkg", [
    ("lsof"),
    ("curl"),
    ("chrony")
])
def test_packages_are_installed(host, pkg):
    package = host.package(pkg)
    assert package.is_installed


@pytest.mark.parametrize("port", [
    (22)
])
def test_service_ports_are_listening(host, port):
    assert host.socket(f"tcp://0.0.0.0:{port}")


@pytest.mark.parametrize("user_id, user_group, user_dir", [
    ("solr", "solr", f"{solr_base_dir}/data/solrhome/alfresco"),
    ("solr", "solr", f"{solr_base_dir}/data/solrhome/archive"),
    ("root", "root", "/tmp/solr")
])
def test_application_directories_exist(host, user_id, user_group, user_dir):
    f = host.file(user_dir)
    assert f.is_directory
    assert f.user == user_id
    assert f.group == user_group
