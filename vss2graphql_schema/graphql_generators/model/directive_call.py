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

from typing import (Iterable, Optional, List, Literal,
                    Callable, Sequence, Union)

from .parameter import Parameter


class DirectiveCall:
    '''
    Class to handle GraphQL directive call
    '''
    name: str
    parameters: Iterable[Parameter]

    def __init__(self, name: str, parameters: Iterable[Parameter]) -> None:
        self.name = name
        self.parameters = parameters

    def __str__(self) -> str:
        r = '@' + self.name
        r += '(' + ', '.join([str(p) for p in self.parameters]) + ')'
        return r


class RangeDirective(DirectiveCall):
    '''
    Range directive call
    '''
    min_value: Optional[Union[int, float]]
    max_value: Optional[Union[int, float]]

    def __init__(
        self, min_value: Optional[Union[int, float]],
        max_value: Optional[Union[int, float]]
    ) -> None:
        parameters: List[Parameter] = []
        if min_value is not None:
            parameters.append(Parameter('min', str(min_value)))
        if max_value is not None:
            parameters.append(Parameter('max', str(max_value)))

        super().__init__('range', parameters)


class DeprecatedDirective(DirectiveCall):
    '''
    Deprecated directive call
    '''
    reason: Optional[str]

    def __init__(self, reason: Optional[str]) -> None:
        parameters: List[Parameter] = []
        if reason:
            p = Parameter('reason', '"' + reason.replace('"', "'") + '"')
            parameters.append(p)
        super().__init__('deprecated', parameters)


Permission = Literal[
    'READ', 'WRITE', 'REALTIME', 'DELIVERY_INTERVAL_1_SECOND',
    'DELIVERY_INTERVAL_5_SECONDS'
]


class HasPermissionsDirective(DirectiveCall):
    '''
    hasPermission Directive Call
    '''
    permissions: Iterable[Permission]

    def __init__(
            self, permissions: Sequence[Permission],
            permission_name: Callable[[Permission], str]
    ) -> None:
        parameters: List[Parameter] = []
        permission_names = [
            '"' + permission_name(p) + '"' for p in permissions
        ]
        if permissions:
            parameters.append(Parameter(
                'permissions', '[' + ', '.join(permission_names) + ']'
            ))
        super().__init__('hasPermissions', parameters)
