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
from typing import TextIO, Iterable, List

from anytree import PreOrderIter

from vspec.model.vsstree import VSSNode

from ..layer import Layer
from ..emitters.mutation_emitter import MutationEmitter
from ..model.field import Field
from ..util import node_has_child_actuator
from ..vss_generators.mutation_generator import MutationGenerator
from ..vss_generators.vss_generator import VSSRootsGenerator


class MutationLayerGenerator(VSSRootsGenerator):
    '''
    Generate GraphQL Mutations for each branch that has one or more actuators
     as children.
    '''
    layer: Layer

    def __init__(
            self, output: TextIO, vss_roots: Iterable[VSSNode],
            args: argparse.Namespace, layer: Layer
    ) -> None:
        '''
        :param output: File to output GraphQL types
        :param vss_roots: roots from VSS tree structure
        '''
        super(MutationLayerGenerator, self).__init__(
            output, 'mutation', MutationEmitter, vss_roots, args
        )
        self.layer = layer

    def _get_entries(self, roots: Iterable[VSSNode]) -> List[Field]:
        '''
        Look for actuators in children and if there is one, create the mutation
        for that node.
        :param roots: all roots from vss
        :return: list of fields in mutation
        '''
        mutation_field = []
        for r in roots:
            for node in PreOrderIter(r):
                if (node.qualified_name('_') in self.layer.write_node_names
                        and node_has_child_actuator(node)):
                    f = MutationGenerator.field_from_vss_node(
                        node,
                    )
                    mutation_field.append(f)
        return mutation_field
