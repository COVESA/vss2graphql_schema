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
from abc import abstractmethod
from typing import (
    TextIO, Optional, Type
)

import jinja2

from .emitters.common_emitter import CommonEmitter
from .templates import Templates


class CommonGenerator:
    '''
    Generator that is supposed to call 'emitter().emit_all()' in the 'generate'
     method.
    It has a 'separator_template' to write a kind of header to organize the
     file it will output.
    '''
    output: TextIO
    name: str
    emitter: Type[CommonEmitter]
    args: argparse.Namespace
    separator_template: jinja2.Template

    def __init__(
            self, output: TextIO, name: str, emitter: Type[CommonEmitter],
            args: argparse.Namespace
    ) -> None:
        self.output = output
        self.name = name
        self.emitter = emitter
        self.args = args
        self.separator_template = getattr(Templates, 'separator')

    def emit_separator(self, name: Optional[str] = None) -> None:
        '''
        Emmits separator on output file using self.separator_template
        :param name: Custom name to print on separator
        :return: None
        '''
        if name is None:
            name = self.name.upper()

        variables = {'section': name}
        self.separator_template.stream(variables).dump(self.output)

    @abstractmethod
    def generate(self) -> None:
        raise NotImplementedError
