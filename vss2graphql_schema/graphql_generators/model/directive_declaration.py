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

from typing import Iterable, Literal, List

from .parameter import Parameter

Location = Literal[
    'SCALAR', 'OBJECT', 'FIELD_DEFINITION', 'ARGUMENT_DEFINITION',
    'INTERFACE', 'UNION', 'ENUM', 'ENUM_VALUE', 'INPUT_OBJECT',
    'INPUT_FIELD_DEFINITION', 'SCHEMA'
]


class DirectiveDeclaration:
    name: str
    parameters: Iterable[Parameter]
    locations: Iterable[Location]

    def __init__(
            self, name: str, parameters: Iterable[Parameter],
            locations: Iterable[Location]
    ) -> None:
        self.name = name
        self.parameters = parameters
        self.locations = locations

    def __str__(self) -> str:
        r = 'directive @' + self.name
        r += '(' + ', '.join([str(p) for p in self.parameters]) + ')'
        r += ' on ' + ' | '.join([str(loc) for loc in self.locations])
        return r


class RangeDirectiveDeclaration(DirectiveDeclaration):
    def __init__(self) -> None:
        parameters: List[Parameter] = [
            Parameter('min', 'Float'), Parameter('max', 'Float')
        ]
        locations: List[Location] = [
            'FIELD_DEFINITION', 'ARGUMENT_DEFINITION', 'INPUT_FIELD_DEFINITION'
        ]
        super().__init__('range', parameters, locations)


class HasPermissionDirectiveDeclaration(DirectiveDeclaration):
    def __init__(self) -> None:
        parameters: List[Parameter] = [
            Parameter('permissions', '[String!]', is_required=True),
            Parameter('policy', 'HasPermissionsDirectivePolicy')
        ]
        locations: List[Location] = [
            'FIELD_DEFINITION', 'OBJECT', 'INPUT_FIELD_DEFINITION'
        ]
        super().__init__('hasPermissions', parameters, locations)
