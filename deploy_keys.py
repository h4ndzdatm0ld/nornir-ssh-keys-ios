from nornir import InitNornir
from nornir_netmiko.tasks import netmiko_send_command
from nornir_utils.plugins.functions import print_result
from nornir_utils.plugins.tasks.data import load_yaml
from nornir_jinja2.plugins.tasks import template_file
from nornir_napalm.plugins.tasks import napalm_validate
from nornir_napalm.plugins.tasks import napalm_get
import os
from nornir_utils.plugins.tasks.files import write_file


__author__ = "Hugo Tinoco"
__email__ = "hugotinoco@icloud.com"

nr = InitNornir("config.yml")

# Filter the hosts by the 'CPE' router type.
cpe_routers = nr.filter(type="CPE")

def validation(task):
    """ Simple getters for documentation of hosts """

    getters = ['get_users', 'get_interfaces_ip', 'get_facts']
    for etter in getters:
        task.run(task=napalm_get, getters=[etter])
        
    write_file(
        task,
        filename=f"{path}/{task.name}-{servicename}.txt",
        content=str(vprn.result),
        append=True,
    )
    # commands = [
    #     f"show ip int brief",
    # ]
    # for cmd in commands:
    #     vprn = task.run(netmiko_send_command, command_string=cmd)
        # write_file(
        #     task,
        #     filename=f"{path}/{task.name}-{servicename}.txt",
        #     content=str(vprn.result),
        #     append=True,
        # )

def main():

    print_result(cpe_routers.run(task=validation))

if __name__ == "__main__":
    main()
