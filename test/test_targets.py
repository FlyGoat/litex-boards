#
# This file is part of LiteX-Boards.
#
# This file is Copyright (c) 2017-2021 Florent Kermarrec <florent@enjoy-digital.fr>
# This file is Copyright (c) 2019 Tim 'mithro' Ansell <me@mith.ro>
# SPDX-License-Identifier: BSD-2-Clause

import subprocess
import unittest
import os

from migen import *

from litex.soc.integration.builder import *

def build_test(socs):
    errors = 0
    for soc in socs:
        os.system("rm -rf build")
        builder = Builder(soc, output_dir="./build", compile_software=False, compile_gateware=False)
        builder.build()
        errors += not os.path.isfile("./build/gateware/top.v")
    os.system("rm -rf build")
    return errors


class TestTargets(unittest.TestCase):
    # Build simple design for all platforms.
    def test_simple(self):
        # Collect platforms.
        platforms = []
        for file in os.listdir("./litex_boards/platforms/"):
            if file.endswith(".py"):
                file = file.replace(".py", "")
                if file not in ["__init__", "qmtech_daughterboard"]:
                    platforms.append(file)

        # Test platforms with simple design.
        for name in platforms:
            with self.subTest(platform=name):
                cmd = """\
python3 -m litex_boards.targets.simple litex_boards.platforms.{} \
    --no-compile-software   \
    --no-compile-gateware   \
    --uart-name="stub"      \
""".format(name)
                subprocess.check_call(cmd, shell=True)
