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
from typing import TextIO

from ..common_generator import CommonGenerator
from ..constants import VSS_CUSTOM_SCALARS_MAPPING
from ..emitters.custom_scalar_emitter import (
    CustomScalarsEmitter
)
from ..model.custom_scalar_declaration import CustomScalarDeclaration


class CustomScalarsGenerator(CommonGenerator):
    '''
    Generate GraphQL custom scalars for types that VSS support but GraphQL
    don't.
    '''
    def __init__(self, output: TextIO, args: argparse.Namespace) -> None:
        super(CustomScalarsGenerator, self).__init__(
            output, 'custom_scalar', CustomScalarsEmitter, args
        )

    def generate(self) -> None:
        '''
        Custom scalars in vss are described in VSS_CUSTOM_TYPES. The custom
        types are fetched there and  sent to emitter.
        :return: List of custom scalars
        '''
        self.emit_separator()

        custom_types = [
            CustomScalarDeclaration(ct, None)
            for ct in VSS_CUSTOM_SCALARS_MAPPING.values()
        ]
        CustomScalarsEmitter(self.output, self.name, custom_types).emit_all()
