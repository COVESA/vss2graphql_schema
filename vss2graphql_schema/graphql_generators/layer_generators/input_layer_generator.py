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
from typing import TextIO, Iterable, List, Mapping, Iterator

from vspec.model.vsstree import VSSNode, VSSType

from ..layer import Layer
from ..util import get_input_name
from ..vss_generators.vss_generator import VSSLeafGenerator
from ..model.field import Field
from ..vss_generators.input_generator import InputEmitter, InputGenerator


class InputLayerGenerator(VSSLeafGenerator):
    '''
    Generate graphql inputs from vss to match Mutations.
    '''
    layer: Layer

    def __init__(
            self, output: TextIO, vss_roots: Iterable[VSSNode],
            args: argparse.Namespace, layer: Layer
    ) -> None:
        super(InputLayerGenerator, self).__init__(
            output, 'input', InputEmitter, vss_roots, args
        )
        self.layer = layer
        self.parent_attrs_input_names = set(
            self.get_layer_parent_attribute_input_node_names()
        )

    def get_layer_parent_attribute_input_node_names(self) -> Iterator[str]:
        for name, entry in self.layer.iterate_qualified_name_value():
            if isinstance(entry, list):
                entry = entry[0]
            if isinstance(entry, dict):
                for child_name, d in entry.items():
                    if isinstance(d, dict):
                        for grandson in d:
                            if '_parentAttribute' in grandson:
                                yield name
                                break

    @staticmethod
    def _get_parents_names(node: VSSNode) -> Iterator[str]:
        node_names = node.qualified_name('_').split('_')
        for i in range(len(node_names)):
            yield '_'.join(node_names[:i + 1])

    def _get_entries(self, node: VSSNode) -> List[Field]:
        '''
        Generate entry for each node child that has type VSSType.ACTUATOR
        :param node: a VSSNode
        :return: List of fields from children with type VSSType.ACTUATOR
        '''
        input_declarations = []
        node_name = node.qualified_name('_')
        if (node_name in self.layer.write_node_names
                or node_name in self.parent_attrs_input_names):
            for child in node.children:
                if child.type == VSSType.ACTUATOR:
                    field = InputGenerator.field_from_vss_node(
                        child, custom_scalars=self.args.custom_scalars,
                        enums=self.args.enums,
                        has_range_directive=self.args.range_directive,
                        has_has_permission_directive=self.args.permission_directive,  # noqa:501
                    )
                    field.description = ''
                    input_declarations.append(field)

                # Add if input child has parent attribute
                if child.qualified_name('_') in self.parent_attrs_input_names:
                    field = InputGenerator.field_from_vss_node(
                        child, custom_scalars=self.args.custom_scalars,
                        enums=self.args.enums, has_range_directive=False,
                        has_has_permission_directive=False,
                    )
                    field.field_type = get_input_name(child)
                    field.description = ''

                    if (child.qualified_name('_')
                            in self.layer.list_node_names):
                        field.field_type = '[' + field.field_type + ']'

                    input_declarations.append(field)

            for parent_name in self._get_parents_names(node):
                if (parent_name in self.layer.list_node_names
                        and len(input_declarations) > 0):
                    id_field = Field('id', 'ID!')
                    input_declarations.append(id_field)

        return input_declarations

    def _get_extra_vars_from_node(self, node: VSSNode) -> Mapping[str, str]:
        return {
            'name': get_input_name(node),
            'description': node.description,
        }
