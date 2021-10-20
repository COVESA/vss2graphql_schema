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

from typing import Optional


class Parameter:
    name: str
    type_or_value: str
    default_value: Optional[str]
    is_required: bool

    def __init__(
            self, name: str, type_or_value: str,
            default_value: Optional[str] = None, is_required: bool = False
    ) -> None:
        self.name = name
        self.type_or_value = type_or_value
        self.default_value = default_value
        self.is_required = is_required

    def __str__(self):
        r = self.name + ': ' + self.type_or_value
        r += '!' if self.is_required else ''
        if self.default_value or self.default_value == '':
            r += ' = ' + self.default_value
        return r
