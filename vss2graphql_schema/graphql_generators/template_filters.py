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

from typing import Mapping, Callable

from .model.description import Description


def _is_blank_line(s: str) -> bool:
    return not bool(len(s.strip('\t \n')))


def indent_spaces(s: str, width: int = 1, blank: bool = False) -> str:
    spaces = '    '
    res = ''
    for r in s.split('\n'):
        if blank and _is_blank_line(r):
            continue
        res = f'{res}{spaces*width}{r}\n'
    return res[:-1]


def description_not_empty(description: Description):
    return not description.empty()


all_filters: Mapping[str, Callable] = {
    'indent_spaces': indent_spaces,
    'description_not_empty': description_not_empty,
}
