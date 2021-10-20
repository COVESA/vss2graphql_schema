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
from typing import TextIO, Iterable, List, Dict

from anytree import LevelOrderIter

from vspec.model.vsstree import VSSNode, VSSType

from .vss_generator import VSSRootsGenerator
from ..emitters.mutation_emitter import MutationEmitter
from ..model.directive_call import DirectiveCall
from ..model.field import Field
from ..model.parameter import Parameter
from ..util import get_input_name, get_mutation_name, get_type_name


class MutationGenerator(VSSRootsGenerator):
    '''
    Generate GraphQL Mutations for each branch that has one or more actuators
     as children.
    '''
    def __init__(
            self, output: TextIO, vss_roots: Iterable[VSSNode],
            args: argparse.Namespace
    ) -> None:
        '''
        :param output: File to output GraphQL types
        :param vss_roots: roots from VSS tree structure
        '''
        super(MutationGenerator, self).__init__(
            output, 'mutation', MutationEmitter, vss_roots, args
        )

    def _get_entries(self, roots: Iterable[VSSNode]) -> List[Field]:
        '''
        Look for actuators in children and if there is one, create the mutation
        for that node.
        :param roots: all roots from vss
        :return: list of fields in mutation
        '''
        mutations: Dict[str, Field] = {}
        for r in roots:
            for node in LevelOrderIter(r):
                if (node.type == VSSType.ACTUATOR and node.parent is not None
                        and node.parent.qualified_name('_') not in mutations):
                    mutations[node.parent.qualified_name('_')] = \
                        self.field_from_vss_node(node.parent)

        return list(mutations.values())

    @staticmethod
    def field_from_vss_node(vss_node: VSSNode) -> Field:
        field_name = get_mutation_name(vss_node)
        field_type = get_type_name(vss_node)
        description = ''

        directives: List[DirectiveCall] = []

        parameters: List[Parameter] = [
            Parameter(
                'input', get_input_name(vss_node),
                is_required=True
            )
        ]

        return Field(
            field_name, field_type, description,
            parameters, directives,
        )
