# Copyright (C) 2021, Bayerische Motoren Werke Aktiengesellschaft (BMW AG),
#   Author: Alexander Domin (Alexander.Domin@bmw.de)
# Copyright (C) 2021, ProFUSION Sistemas e Soluções LTDA,
#   Author: Leonardo Ramos (leo.ramos@profusion.mobi)
#
# SPDX-License-Identifier: MPL-2.0
#
# This Source Code Form is subject to the terms of the
# Mozilla Public License, v. 2.0. If a copy of the MPL was
# not distributed with this file, You can obtain one at
# http://mozilla.org/MPL/2.0/.

import argparse
from typing import TextIO, List

from ..common_generator import CommonGenerator
from ..emitters.directive_emitter import DirectiveEmitter
from ..model.directive_declaration import (
    DirectiveDeclaration, RangeDirectiveDeclaration,
    HasPermissionDirectiveDeclaration,
)
from ..templates import Templates


class DirectiveGenerator(CommonGenerator):
    '''
    Generate declarations for hasPermission and range directive.
    For now directives are manually put in directives_open.jinja.
    '''
    def __init__(self, output: TextIO, args: argparse.Namespace) -> None:
        super(DirectiveGenerator, self).__init__(
            output, 'directive', DirectiveEmitter, args
        )

    def generate(self) -> None:
        directives: List[DirectiveDeclaration] = []

        if self.args.range_directive:
            directives.append(RangeDirectiveDeclaration())

        if self.args.permission_directive:
            directives.append(HasPermissionDirectiveDeclaration())

        if directives:
            self.emit_separator()

            if self.args.permission_directive:
                template = getattr(Templates, 'permission_enum')
                template.stream().dump(self.output)

            DirectiveEmitter(self.output, self.name, directives).emit_all()
