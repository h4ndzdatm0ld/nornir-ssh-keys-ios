from nornir import InitNornir
from nornir_netmiko.tasks import netmiko_send_command
from nornir_utils.plugins.functions import print_result
from nornir_utils.plugins.tasks.data import load_yaml
from nornir_jinja2.plugins.tasks import template_file
from nornir_napalm.plugins.tasks import napalm_validate
from nornir_napalm.plugins.tasks import napalm_get
import os
import subprocess
import getpass
from nornir_utils.plugins.tasks.files import write_file
from jaraco.docker import is_docker

__author__ = "Hugo Tinoco"
__email__ = "hugotinoco@icloud.com"

nr = InitNornir("config.yml")

# Filter the hosts by the 'CPE' router type.
cpe_routers = nr.filter(type="CPE")

def createFolder(directory):
    try:
        if not os.path.exists(directory):
            os.makedirs(directory)
    except OSError:
        print("Error: Creating directory. " + directory)


def validation(task):
    """ Simple getters for documentation of hosts """

    getters = ['get_users', 'get_interfaces_ip', 'get_facts']

    for getter in getters:
        data = task.run(task=napalm_get, getters=[getter])

        # Path to save output: This path will be generated.
        path = f"Output/{task.host.platform}"
        createFolder(path)
        
        write_file(
            task,
            filename=f"{path}/{task.name}-{task.host}.txt",
            content=str(data.result)+'\n',
            append=True,
        )

def subprocess_keys():
    """ Fold the ssh public key and store the contents. This is outside of Nornir, as we only 
    need to extract the ssh-key once for the entire runbook."""

    # Extract Username:
    username = getpass.getuser()
    # Capture the folder key for the current user.
    # This program assumes default directory of ssh keys.

    if is_docker:
        key = subprocess.run(['fold', '-b', '-w 72', f'/home/{username}/.ssh/id_rsa.pub'], capture_output=True)
        return key.stdout
    else:
        key = subprocess.run(['fold', '-b', '-w 72', f'/Users/{username}/.ssh/id_rsa.pub'], capture_output=True)
        return key.stdout

def configure_key(task, folded_key):
    """ Deploy SSH Keys """

    pass
    # commands = [
    #     f"show ip int brief",
    # ]
    # for cmd in commands:
    #     vprn = task.run(netmiko_send_command, command_string=cmd)~~
        # write_file(
        #     task,
        #     filename=f"{path}/{task.name}-{servicename}.txt",
        #     content=str(vprn.result),
        #     append=True,
        # )

def main():


    # print_result(cpe_routers.run(task=validation))
    print_result(cpe_routers.run(task=configure_key, folded_key=subprocess_keys()))

if __name__ == "__main__":
    main()
