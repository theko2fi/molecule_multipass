#  Copyright (c) 2023 Kenneth KOFFI
#
#  Permission is hereby granted, free of charge, to any person obtaining a copy
#  of this software and associated documentation files (the "Software"), to
#  deal in the Software without restriction, including without limitation the
#  rights to use, copy, modify, merge, publish, distribute, sublicense, and/or
#  sell copies of the Software, and to permit persons to whom the Software is
#  furnished to do so, subject to the following conditions:
#
#  The above copyright notice and this permission notice shall be included in
#  all copies or substantial portions of the Software.
#
#  THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
#  IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
#  FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
#  AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
#  LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
#  FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
#  DEALINGS IN THE SOFTWARE.
"""Multipass Driver Module."""


import os

from molecule import logger
from molecule.api import Driver
from molecule.util import sysexit_with_message
from shutil import which

log = logger.get_logger(__name__)


class Multipass(Driver):
    """
    Multipass Driver Class.

    The class responsible for managing `Multipass`_ virtual machines.

    Molecule leverages Ansible's `theko2fi.multipass.multipass_vm`_ module, by mapping
    variables from ``molecule.yml`` into ``create.yml`` and ``destroy.yml``.

    .. _`theko2fi.multipass.multipass_vm`: https://theko2fi.github.io/ansible-multipass-collection/branch/main/multipass_vm_module.html

    .. code-block:: yaml

        driver:
          name: molecule_multipass
        platforms:
          - name: instance

    .. code-block:: bash

        $ python3 -m pip install molecule_multipass

    """

    _passed_sanity = False

    def __init__(self, config=None) -> None:
        """Construct Multipass."""
        super().__init__(config)
        self._name = "molecule_multipass"

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        self._name = value

    @property
    def login_cmd_template(self):
        return (
            "multipass exec {instance} -- bash"
        )

    @property
    def default_safe_files(self):
        return []

    @property
    def default_ssh_connection_options(self):
        return []

    def login_options(self, instance_name):
        return {"instance": instance_name}

    def ansible_connection_options(self, instance_name):
        x = {"ansible_connection": "theko2fi.multipass.multipass"}
        return x

    def sanity_checks(self):
        """Implement Multipass driver sanity checks."""
        if self._passed_sanity:
            return

        log.info("Sanity checks: '%s'", self._name)
        # try:
        #     from multipass import MultipassClient

        #     multipass_client = MultipassClient()
        #     multipass_client.list()
        # except Exception as e:
        #     msg = (
        #         "Unable to contact the Multipass daemon. "
        #         "Please refer to https://ddsfgdgdg/ "
        #         "for managing the daemon"
        #     )
        #     sysexit_with_message(msg)
        
        if not which("multipass"):
          sysexit_with_message("multipass executable was not found!")

        self._passed_sanity = True

    def reset(self):
      pass


    @property
    def required_collections(self) -> dict[str, str]:
        """Return collections dict containing names and versions required."""
        # https://galaxy.ansible.com/community/docker
        return {"theko2fi.multipass": "0.1.0"}
