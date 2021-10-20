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
from typing import List, TextIO, Iterable, Mapping, Iterator

from vspec.model.vsstree import VSSNode

from ..layer import Layer
from ..util import get_type_name
from ..vss_generators.type_generator import TypeGenerator
from ..vss_generators.vss_generator import VSSLeafGenerator
from ..emitters.type_field_emitter import TypeFieldEmitter
from ..model.field import Field


class TypeLayerGenerator(VSSLeafGenerator):
    '''
    Generate GraphQL types for each structure in VSS. Custom types are created
     for branches and scalar types are translated inside
     FieldDeclaration.from_vss_node.
    '''
    layer: Layer

    def __init__(
            self, output: TextIO, vss_roots: Iterable[VSSNode],
            args: argparse.Namespace, layer: Layer
    ) -> None:
        '''
        :param output: File to output GraphQL types
        :param vss_roots: roots from VSS tree structure
        :param custom_scalars: Whether it will use custom scalars from VSS
        '''
        super(TypeLayerGenerator, self).__init__(
            output, 'type', TypeFieldEmitter, vss_roots, args
        )
        self.layer = layer

    def get_list_node_names(self) -> Iterator[str]:
        for name, layer_entry in self.layer.iterate_qualified_name_value():
            if isinstance(layer_entry, list):
                yield name

    def _get_entries(self, node: VSSNode) -> List[Field]:
        '''
        Get fields from each node.
        :param node: a VSSNode
        :return: List of fields that will be included in GraphQL type
        '''
        children_declarations: List[Field] = []

        for child in node.children:
            field = TypeGenerator.field_from_vss_node(
                child, custom_scalars=self.args.custom_scalars,
                enums=self.args.enums,
                has_range_directive=self.args.range_directive,
                has_has_permission_directive=self.args.permission_directive,
            )

            if child.qualified_name('_') in self.layer.list_node_names:
                field.field_type = '[' + field.field_type + ']'

            children_declarations.append(field)

        if (node.qualified_name('_') in self.layer.list_node_names
                and len(children_declarations) > 0):
            id_field = Field('id', 'ID!')
            children_declarations.append(id_field)

        return children_declarations

    def _get_extra_vars_from_node(self, node: VSSNode) -> Mapping[str, str]:
        return {
            'name': get_type_name(node),
            'description': node.description,
        }
