#!/bin/bash
# Molecule shortcut over molecule inside container
# Coming from: https://gist.github.com/fletort/7a34c7f211acf0cde56c8f2749a3ec8b
# Use ./molecule.sh shell to login on the container bash

if [ "$1" = "shell" ] ; then
    docker run --rm -it \
        -v $(pwd):/tmp/$(basename "${PWD}") \
        -v /var/run/docker.sock:/var/run/docker.sock \
        -v ~/.cache/:/root/.cache/ \
        -v ~/.ssh:/root/.ssh \
        -w /tmp/$(basename "${PWD}") \
        -e HOST_PWD=$(PWD) \
        --name molecule \
        quay.io/ansible/molecule:3.0.6 \
        sh
else
    docker run --rm -it \
        -v $(pwd):/tmp/$(basename "${PWD}") \
        -v /var/run/docker.sock:/var/run/docker.sock \
        -v ~/.cache/:/root/.cache/ \
        -v ~/.ssh:/root/.ssh \
        -w /tmp/$(basename "${PWD}") \
        -e HOST_PWD=$(PWD) \
        --name molecule \
        quay.io/ansible/molecule:3.0.6 \
        molecule "$@"
fi

# Explanation:
# -v $(pwd):/tmp/$(basename "${PWD}")
# This option is used to share the current project directory with the 
# container in the /tmp/<project_dir> directory. <project_dir> is the name
# of the project directory on the host (where this script is located)
#
# -w /tmp/$(basename "${PWD}")
# This option is used to make the directory shared previsouly the
# default (starting/working) directory of the container
#
# /var/run/docker.sock:/var/run/docker.sock
# This option gives the possibility to create docker container from 
# the molecule container (docker-in-docker), using the host docker.
#
# -v ~/.cache/:/root/.cache/
# This option is used to keep molecule context  (all molecule cache files)
# between successive creation/execution/deletion of the molecule container.
#
# -v ~/.ssh:/root/.ssh
# This option is used to get all ssh context (known hosts, keys)
# of the host.
#
# -e HOST_PWD=$(PWD)
# This option is usefull to have the Host PWD information inside the molecule
# container. We need this information, in following context: if we run a new
# docker container from the molecule container (docker in docker) with
# sharing filesystem process. If we are using the PWD variable in this
# sharing filesystem process, it will be equal to /tmp/<project_dir>,
# (current directory in the molecule container). But the conainer 
# will be creaeted in the host context, where this directory does not
# exist... So user must use HOST_PWD instead of PWD in the sharing process.
#
# --name molecule
# created container will be named "molecule"
#
# quay.io/ansible/molecule:3.0.6
# This is the image used to create the container

