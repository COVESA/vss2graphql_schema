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
from typing import TextIO, Iterable, List, Mapping, Any

from vspec.model.vsstree import VSSNode, VSSType

from .vss_generator import VSSLeafGenerator
from ..emitters.input_emitter import InputEmitter
from ..model.directive_call import DirectiveCall, Permission, \
    HasPermissionsDirective
from ..model.field import Field
from ..model.parameter import Parameter
from ..util import (
    to_lower_camel_case, get_field_type, get_node_description,
    get_range_directive, get_input_name,
)


class InputGenerator(VSSLeafGenerator):
    '''
    Generate graphql inputs from vss to match Mutations.
    '''
    def __init__(
            self, output: TextIO, vss_roots: Iterable[VSSNode],
            args: argparse.Namespace
    ) -> None:
        super(InputGenerator, self).__init__(
            output, 'input', InputEmitter, vss_roots, args
        )

    def _get_entries(self, node: VSSNode) -> List[Field]:
        '''
        Generate entry for each node child that has type VSSType.ACTUATOR
        :param node: a VSSNode
        :return: List of fields from children with type VSSType.ACTUATOR
        '''
        input_declarations = []
        for child in node.children:
            if child.type == VSSType.ACTUATOR:
                input_declarations.append(self.field_from_vss_node(
                    child, custom_scalars=self.args.custom_scalars,
                    enums=self.args.enums,
                    has_range_directive=self.args.range_directive,
                    has_has_permission_directive=self.args.permission_directive,  # noqa: 501
                ))

        return input_declarations

    def _get_extra_vars_from_node(self, node: VSSNode) -> Mapping[str, Any]:
        return {
            'name': get_input_name(node),
            'description': get_node_description(node, not self.args.enums),
        }

    @staticmethod
    def field_from_vss_node(
            vss_node: VSSNode, custom_scalars: bool = False,
            enums: bool = False, has_range_directive: bool = False,
            has_has_permission_directive: bool = False,

    ) -> Field:
        field_name = to_lower_camel_case(vss_node.name)
        field_type = get_field_type(vss_node, custom_scalars, enums)
        description = get_node_description(vss_node, not enums)

        directives: List[DirectiveCall] = []

        if has_range_directive:
            range_directive = get_range_directive(vss_node)
            if range_directive:
                directives.append(range_directive)

        if has_has_permission_directive:
            def pname(x: Permission) -> str:
                return vss_node.qualified_name('.') + '_' + x
            directives.append(HasPermissionsDirective(['WRITE'], pname))

        parameters: List[Parameter] = []

        return Field(
            field_name, field_type, description,
            parameters, directives,
        )
