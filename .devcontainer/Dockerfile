# See here for image contents: https://github.com/microsoft/vscode-dev-containers/tree/v0.158.0/containers/ubuntu/.devcontainer/base.Dockerfile

# [Choice] Ubuntu version: bionic, focal
ARG VARIANT="focal"
FROM mcr.microsoft.com/vscode/devcontainers/base:0-${VARIANT}
ENV DEBIAN_FRONTEND noninteractive
# [Optional] Uncomment this section to install additional OS packages.
RUN apt-get update && export DEBIAN_FRONTEND=noninteractive \
    && apt-get -y install --no-install-recommends \
    && apt-get upgrade  -y \
    && apt-get install python3 \
    && apt-get install python3-pip -y \
    && apt-get -y install openssh-client 

RUN useradd -m cisco
RUN mkdir -p /home/cisco/.ssh
RUN chown -R cisco:cisco /home/cisco/.ssh
RUN echo "Host remotehost\n\tStrictHostKeyChecking no\n" >> /home/cisco/.ssh/config
RUN echo "    KexAlgorithms diffie-hellman-group1-sha1,curve25519-sha256@libssh.org,ecdh-sha2-nistp256,ecdh-sha2-nistp384,ecdh-sha2-nistp521,diffie-hellman-group-exchange-sha256,diffie-hellman-group14-sha1" >> /etc/ssh/ssh_config
RUN ssh-keygen -q -t rsa -N '' -f /id_rsa
RUN mv id_rsa /home/cisco/.ssh
RUN mv id_rsa.pub /home/cisco/.ssh
USER cisco
