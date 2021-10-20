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

from typing import TypeVar, Generic, TextIO, Iterable

import jinja2

from ..templates import Templates

TEntry = TypeVar('TEntry')


class CommonEmitter(Generic[TEntry]):
    '''
    Emitter responsible for writing in a file 'output' based on the jinja
     templates for open, entry and close.
    '''
    output: TextIO
    name: str
    entries: Iterable[TEntry]
    close_template: jinja2.Template
    entry_template: jinja2.Template
    open_template: jinja2.Template

    def __init__(
        self,
        output: TextIO,
        name: str,
        entries: Iterable[TEntry],
    ) -> None:
        self.output = output
        self.name = name
        self.entries = entries
        self.close_template = getattr(Templates, f'{name}_close')
        self.entry_template = getattr(Templates, f'{name}_entry')
        self.open_template = getattr(Templates, f'{name}_open')

    def emit_open(self, extra_vars=None) -> None:
        if extra_vars is None:
            extra_vars = {}

        variables = {}
        if extra_vars:
            variables.update(extra_vars)
        self.open_template.stream(variables).dump(self.output)

    def emit_close(self, extra_vars=None) -> None:
        if extra_vars is None:
            extra_vars = {}

        variables = {}
        if extra_vars:
            variables.update(extra_vars)
        self.close_template.stream(variables).dump(self.output)

    def emit_entry(
        self,
        entry: TEntry,
            extra_vars=None,
    ) -> None:
        if extra_vars is None:
            extra_vars = {}

        variables = {'entry': entry}
        if extra_vars:
            variables.update(extra_vars)
        self.entry_template.stream(variables).dump(self.output)

    def emit_all_entries(self, extra_vars=None) -> None:
        if extra_vars is None:
            extra_vars = {}

        for entry in self.entries:
            self.emit_entry(entry, extra_vars)

    def emit_all(self, extra_vars=None) -> None:
        if extra_vars is None:
            extra_vars = {}

        self.emit_open(extra_vars)
        self.emit_all_entries(extra_vars)
        self.emit_close(extra_vars)
