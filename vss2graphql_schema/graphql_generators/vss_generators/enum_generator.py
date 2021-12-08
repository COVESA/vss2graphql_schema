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
from typing import TextIO, Iterable, List, Mapping, Iterator, Any

from vspec.model.vsstree import VSSNode

from .vss_generator import VSSLeafGenerator
from ..emitters.enum_emitter import EnumFieldEmitter
from ..model.enum_field import EnumField
from ..model.description import Description
from ..util import (str_as_uppercase_variable, node_has_enum,
                    get_enum_name, get_node_description)


class EnumGenerator(VSSLeafGenerator):
    '''
    Generate GraphQL enums from vss.
    Enums are fetched from node.enum (a string formatted as a list of strings).
    '''

    def __init__(
            self, output: TextIO, node: Iterable[VSSNode],
            args: argparse.Namespace
    ) -> None:
        super().__init__(output, 'enum', EnumFieldEmitter, node, args)

    def _get_entries(self, node: VSSNode) -> List[EnumField]:
        '''
        Entry from node.enum split
        :param node: node to search for enum
        :return: List of EnumFields
        '''

        return list(self.fields_from_node(node))

    def _get_extra_vars_from_node(self, node: VSSNode) -> Mapping[str, Any]:
        return {
            'name': get_enum_name(node),
            'description': get_node_description(node, not self.args.enums),
        }

    @staticmethod
    def fields_from_node(node: VSSNode) -> Iterator[EnumField]:
        '''
        Iterator of enums inside a node
        :param node: Node to search for the enum
        :return: Next EnumField found in node
        '''
        if node_has_enum(node):
            # Python is handling the conversion from str to list
            enum_list = [e.upper() for e in list(node.enum)]
            enum_seen = set()
            for e in enum_list:
                if e not in enum_seen:
                    enum_seen.add(e)
                    yield EnumField(
                        str_as_uppercase_variable(e), Description('')
                    )
