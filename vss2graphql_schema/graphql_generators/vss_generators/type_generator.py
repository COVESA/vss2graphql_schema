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
from typing import List, TextIO, Iterable, Mapping, Any

from vspec.model.vsstree import VSSNode

from .vss_generator import VSSLeafGenerator
from ..constants import VSS_BRANCH_TYPES
from ..emitters.type_field_emitter import TypeFieldEmitter
from ..model.directive_call import DirectiveCall
from ..model.field import Field
from ..model.parameter import Parameter
from ..util import (
    to_lower_camel_case, get_field_type, get_node_description,
    get_range_directive, get_deprecation_directive, get_type_name,
    get_has_permission_directive
)


class TypeGenerator(VSSLeafGenerator):
    '''
    Generate GraphQL types for each structure in VSS. Custom types are created
     for branches and scalar types are translated inside
     FieldDeclaration.from_vss_node.
    '''

    def __init__(
            self, output: TextIO, vss_roots: Iterable[VSSNode],
            args: argparse.Namespace
    ) -> None:
        '''
        :param output: File to output GraphQL types
        :param vss_roots: roots from VSS tree structure
        :param custom_scalars: Whether it will use custom scalars from VSS
        '''
        super(TypeGenerator, self).__init__(
            output, 'type', TypeFieldEmitter, vss_roots, args
        )

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
            children_declarations.append(field)
        return children_declarations

    def _get_extra_vars_from_node(self, node: VSSNode) -> Mapping[str, Any]:
        return {
            'name': get_type_name(node),
            'description': get_node_description(node),
        }

    @staticmethod
    def field_from_vss_node(
            vss_node: VSSNode, custom_scalars: bool = False,
            enums: bool = False, has_range_directive: bool = False,
            has_has_permission_directive: bool = False,
    ) -> Field:
        field_name = to_lower_camel_case(vss_node.name)
        field_type = get_field_type(vss_node, custom_scalars, enums)
        description = get_node_description(vss_node)

        directives: List[DirectiveCall] = []

        deprecation_directive = get_deprecation_directive(vss_node)
        if deprecation_directive:
            directives.append(deprecation_directive)

        if has_range_directive:
            range_directive = get_range_directive(vss_node)
            if range_directive:
                directives.append(range_directive)

        if (has_has_permission_directive
           and vss_node.type not in VSS_BRANCH_TYPES):
            has_permission_directive = get_has_permission_directive(
                vss_node, ['READ']
            )
            if has_permission_directive:
                directives.append(has_permission_directive)

        parameters: List[Parameter] = []

        return Field(
            field_name, field_type, description,
            parameters, directives,
        )
