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

import re
from typing import Optional, TextIO, Sequence

import yaml

import yamlinclude

from anytree import LevelOrderIter

from vspec import VSSNode
from vspec.model.vsstree import VSSType

from .constants import (
    VSS_GQL_TYPE_MAPPING, VSS_GQL_CUSTOM_TYPE_MAPPING, VSS_BRANCH_TYPES
)
from .model.directive_call import RangeDirective, DeprecatedDirective, \
    HasPermissionsDirective, Permission

READER_TABLE = [
    (re.compile(r'^.+\.depl$', re.IGNORECASE), yamlinclude.YamlReader),
]

NON_UPPERCASE = re.compile(r'[^A-Z]')
LOWER_CAMEL_CASE = re.compile(r'[\-_.\s]([a-z])')
NON_ALPHANUMERIC_WORD = re.compile('[^A-Za-z0-9]+')


def to_lower_camel_case(field: str) -> str:
    '''
    Transform type field to lowerCamelCase
    :param field: Any string to be transformed
    :return: A string in lowerCamelCase
    '''
    last_to_lower = max(1, r.start() - 1) if (
        r := NON_UPPERCASE.search(field)
    ) else len(field)

    return field[:last_to_lower].lower() + LOWER_CAMEL_CASE.sub(
        lambda matched: matched.group(1).upper(), field[last_to_lower:]
    )


def str_as_variable(word: str) -> str:
    '''
    Set word as a variable name, removing non-alphanumeric characters and
    starting with '_' if it starts with a digit.
    :param word: any string
    :return: a string formatted as a variable name for GraphQL
    '''
    variable_name = NON_ALPHANUMERIC_WORD.sub('_', word)
    if word[0].isdigit():
        return '_' + variable_name
    return variable_name


def str_as_uppercase_variable(word: str) -> str:
    '''
    Set word as a variable name, removing non-alphanumeric characters and
    starting with '_' if it starts with a digit.
    :param word: any string
    :return: a string formatted as a upper case variable name for GraphQL
    '''
    return str_as_variable(word).upper()


def get_enum_name(node: VSSNode):
    '''
    :param node: Node to get enum name
    :return: A string with the standard enum name for the node entered.
    '''
    return node.qualified_name('_') + '_Enum'


def get_input_name(node: VSSNode):
    '''
    :param node: Node to get input name
    :return: A string with the standard input name for the node entered.
    '''
    return node.qualified_name('_') + '_Input'


def get_mutation_name(node: VSSNode):
    '''
    :param node: Node to get mutation name
    :return: A string with the standard mutation name for the node entered.
    '''
    return 'set' + node.qualified_name('')


def get_type_name(node: VSSNode):
    '''
    :param node: Node to get type name
    :return: A string with the standard type name for the node entered.
    '''
    return node.qualified_name('_')


def node_has_enum(node: VSSNode) -> bool:
    '''
    :param node: Node to check enum
    :return: True if node has VSS enum.
    '''
    return node.enum and node.enum != ''


def get_field_type(
        node: VSSNode, custom_scalars: bool = False, enums: bool = False
) -> str:
    '''
    :param node: Node to check type
    :param custom_scalars: Flag to consider if is using custom scalars
    :param enums: Flag to consider if is using enums
    :return: GraphQL field type of the node entered
    '''
    if custom_scalars:
        type_mapping = VSS_GQL_CUSTOM_TYPE_MAPPING
    else:
        type_mapping = VSS_GQL_TYPE_MAPPING

    if enums and node_has_enum(node):
        return get_enum_name(node)
    if node.type in VSS_BRANCH_TYPES:
        return node.qualified_name('_')
    else:
        return type_mapping[node.data_type]


def get_node_description(node: VSSNode) -> str:
    '''
    :param node: Node to get description
    :return: Nodes description
    '''
    if node.type in VSS_BRANCH_TYPES:
        return ''
    return node.description


def get_range_directive(node: VSSNode) -> Optional[RangeDirective]:
    '''
    Generate a RangeDirective from a node
    :param node: Node to check directive
    :return: RangeDirective with boundaries if node has one, else None
    '''
    range_min = float(node.min) if node.min != '' else None
    range_max = float(node.max) if node.max != '' else None

    if range_min or range_max:
        return RangeDirective(range_min, range_max)
    return None


def get_has_permission_directive(
        node: VSSNode, permissions: Sequence[Permission],
) -> HasPermissionsDirective:
    def pname(x: Permission) -> str:
        return node.qualified_name('.') + '_' + x

    return HasPermissionsDirective(permissions, pname)


def get_subscription_has_permission_directive(
        node: VSSNode, permissions: Sequence[Permission],
) -> HasPermissionsDirective:
    def pname(x: Permission) -> str:
        return 'Subscription.' + node.qualified_name('.') + '.' + x

    return HasPermissionsDirective(permissions, pname)


def get_deprecation_directive(node: VSSNode) -> Optional[DeprecatedDirective]:
    '''
    Generate DeprecationDirective from the string node.directive
    :param node: Node to get directive
    :return: DeprecationDirective if node has deprecation, else None
    '''
    if node.deprecation and node.deprecation != '':
        return DeprecatedDirective(node.deprecation)
    return None


def sort_children(root: VSSNode) -> None:
    '''
    Sort children on every node
    :param root: Tree root to sort children
    :return: None
    '''
    for node in LevelOrderIter(root):
        node.children = sorted(
            node.children, key=lambda x: x.qualified_name('_'),
        )


def node_has_child_actuator(node: VSSNode) -> bool:
    '''
    :param node: Node to check
    :return: True if one of node's children has an actuator
    '''
    for child in node.children:
        if child.type == VSSType.ACTUATOR:
            return True
    return False


def load_yaml(root_file: TextIO, base_dir: str) -> dict:
    '''
     :param root_file: TextIOWrapper
            It should contain the other files and fields to be included with
            the sintax !include: other.depl file. The other files may be fields
            or include other depl files.
     :param base_dir: str
            Directory that contains the root depl file
     :return: dict
            Nested dictionary with the data of the parsed layer files.
    '''
    yamlinclude.YamlIncludeConstructor.add_to_loader_class(
        loader_class=yaml.FullLoader,
        base_dir=base_dir,
        reader_map=READER_TABLE
    )
    return yaml.load(root_file, Loader=yaml.FullLoader)
