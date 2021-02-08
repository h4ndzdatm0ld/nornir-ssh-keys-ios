from nornir import InitNornir
from nornir_netmiko.tasks import netmiko_send_command
from nornir_netmiko.tasks import netmiko_send_config
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


def subprocess_keys():
    """Fold the ssh public key and store the contents. This is outside of Nornir, as we only
    need to extract the ssh-key once for the entire runbook."""

    # Extract Username:
    username = getpass.getuser()
    # Capture the folder key for the current user.
    # This program assumes default directory of ssh keys.

    if is_docker:
        key = subprocess.run(
            ["fold", "-b", "-w 72", f"/home/{username}/.ssh/id_rsa.pub"],
            capture_output=True,
        )
    else:
        key = subprocess.run(
            ["fold", "-b", "-w 72", f"/Users/{username}/.ssh/id_rsa.pub"],
            capture_output=True,
        )
    # The key is returned as a bytestring, we must decode it to a str.
    key_output = key.stdout
    return str(key_output.decode("utf-8"))


def configure_key(task, folded_key: str):
    """ Deploy SSH Keys to our inventory. The folded_key is passed is as an arguement equal to the result of the subprocess_keys() fucntion.
    In a production environment, a user is most likely already configured on the devices."""

    commands = [
        "enable",
        "config t",
        "ip ssh pubkey-chain",
        f"username {task.host.username}",
        "key-string",
        folded_key,
        "exit",
        "exit",
    ]

    # Path to save output: This path will be generated.
    path = f"Output/{task.host.platform}"
    createFolder(path)

    for cmd in commands:
        passwordless = task.run(
            netmiko_send_command,
            command_string=cmd, 
            use_timing=True,
            delay_factor=1,
        )
        write_file(
            task,
            filename=f"{path}/{task.name}-{task.host}.txt",
            content=str(passwordless.result),
            append=True,
        )


def validation(task):
    """Simple getters for documentation of hosts. This step will be performed via NAPALM using SSH KEYS authentication,
    thus validating the SSH KEYS deployment. We will also do some compliance verification of facts to display ssh keys for users"""

    getters = ["get_users", "get_interfaces_ip", "get_facts"]

    for getter in getters:
        data = task.run(task=napalm_get, getters=[getter])

        write_file(
            task,
            filename=f"Output/{task.name}-{task.host}.txt",
            content=str(data.result) + "\n",
            append=True,
        )

        # Validate part of the SSH-KEY HASH is present.
        if getter == 'get_users':
            assert "4A9CD818E244F2C6B861F2B3C427E80F " in str(data.result)

def main():

    # print_result(cpe_routers.run(task=configure_key, folded_key=subprocess_keys()))
    print_result(cpe_routers.run(task=validation))


if __name__ == "__main__":
    main()
