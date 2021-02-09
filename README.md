# nornir-ssh-keys-ios
Use Nornir3 to distribute and configure passwordless ssh logins to Cisco IOS Routers.

+ Assumptions:
    - SSH User account already configured on the devices.
    - IP Connectivity
    - SSH Keys have already been generated

+ Review the Groups File. Update your Username/Password. Ensure the correct ssh key file parameters are updated to match your environment.

## Nornir Groups File 
---
IOS:
  username: "UPDATE ME" <------ Update this value.
  password: "UPDATE ME" <------ Update this value.
  platform: ios
  port: 22
  connection_options:
    napalm:
      platform: ios
      username: "UPDATE ME" <------ Update this value.
      extras:
        optional_args:
          alt_host_keys: True <------ Update this value.
          # key_file: ~/.ssh/id_rsa <------ Update this value.
          alt_key_file: /home/cisco/.ssh/id_rsa <------ Update this value.
          use_keys: True

# Testing via Docker
Start the tool from the dockerfile in .dev.
Install the requirements. (Opted out of doing this via dockerfile.)
A new home dir will be created, 'home/cisco/' and a key will be generated and placed in the '/home/cisco/.ssh/' folder.

- Quickly create a new key to test and deploy a new identity against your test device.

    sudo ssh-keygen -q -t rsa -N '' -f /home/cisco/.ssh/id_rsa