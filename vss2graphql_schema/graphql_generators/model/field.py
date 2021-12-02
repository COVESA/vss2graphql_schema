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

from typing import Optional, Sequence

from .description import Description
from .directive_call import DirectiveCall
from .parameter import Parameter


class Field:
    '''
    Class that holds multiple info for declarations as
     "field_name: field_type directives"
    '''
    field_name: str
    field_type: str
    description: Optional[Description]
    parameters: Sequence[Parameter]
    directives: Sequence[DirectiveCall]

    def __init__(
            self, field_name: str, field_type: str,
            description: Optional[Description] = None,
            parameters: Optional[Sequence[Parameter]] = None,
            directives: Optional[Sequence[DirectiveCall]] = None,
    ) -> None:
        self.field_name = field_name
        self.field_type = field_type
        self.description = description if description else Description('')
        self.parameters = parameters if parameters else []
        self.directives = directives if directives else []

    def __str__(self) -> str:
        r = self.field_name
        if len(self.parameters) > 0:
            r += '(' + ', '.join([str(p) for p in self.parameters]) + ')'
        r += ': ' + self.field_type

        if len(self.directives) > 0:
            r += ' ' + ' '.join([str(d) for d in self.directives])
        return r
