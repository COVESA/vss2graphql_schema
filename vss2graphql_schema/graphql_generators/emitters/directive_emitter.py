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

from typing import TextIO, Iterable

from .common_emitter import CommonEmitter
from ..model.directive_declaration import DirectiveDeclaration


class DirectiveEmitter(CommonEmitter):
    def __init__(
            self,
            output: TextIO,
            name: str,
            entries: Iterable[DirectiveDeclaration],
    ) -> None:
        super().__init__(output, name, entries)
