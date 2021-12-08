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
from typing import TextIO, Iterable, List, Iterator

from vspec.model.vsstree import VSSNode

from .vss_generator import VSSRootsGenerator
from ..emitters.query_emitter import QueryEmitter
from ..model.directive_call import DirectiveCall
from ..model.field import Field
from ..model.parameter import Parameter
from ..util import to_lower_camel_case, get_field_type, get_node_description


class QueryGenerator(VSSRootsGenerator):
    '''
    Generates a GraphQL query for each root in VSS.
    '''
    def __init__(
            self, output: TextIO, vss_roots: Iterable[VSSNode],
            args: argparse.Namespace
    ) -> None:
        '''
        :param output: File to output GraphQL Query
        :param vss_roots: roots from VSS tree structure
        '''
        super(QueryGenerator, self).__init__(
            output, 'query', QueryEmitter, vss_roots, args
        )

    def __iter__(self) -> Iterator[Iterable[VSSNode]]:
        '''
        Default iteration for Query is to get all roots, since there is only
        one query on schema.
        :return: the roots
        '''
        yield self.vss_roots

    def _get_entries(self, roots: Iterable[VSSNode]) -> List[Field]:
        return [
            QueryGenerator.field_from_vss_node(r) for r in roots
        ]

    @staticmethod
    def field_from_vss_node(
            vss_node: VSSNode, custom_scalars: bool = False,
            enums: bool = False,
    ) -> Field:

        field_name = to_lower_camel_case(vss_node.name)
        field_type = get_field_type(vss_node, custom_scalars, enums)
        description = get_node_description(vss_node, not enums)

        directives: List[DirectiveCall] = []
        parameters: List[Parameter] = []

        return Field(
            field_name, field_type, description,
            parameters, directives,
        )
