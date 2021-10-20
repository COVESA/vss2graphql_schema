#!/usr/bin/env python3

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

from vspec import load_tree

from .graphql_generators.util import sort_children
from .graphql_generators.layer import Layer
from .graphql_generators.node_filters.layer_filter import create_layer_filter
from .graphql_generators.graphql_schema_vss_layer import (
    GraphQLSchemaVSSLayer
)
from .graphql_generators.node_filters.vss_tree_filter import VSSTreeFilter
from .graphql_generators.node_filters.regex_filter import (
    create_match_pattern, create_filter_pattern
)
from .graphql_generators.graphql_schema_vss import (
    GraphQLSchemaVSS
)


def get_arg_parse() -> argparse.ArgumentParser:

    parser = argparse.ArgumentParser(
        description='vss2graphql_schema is a program which generates a'
                    ' GraphQL schema file from the vehicle signal '
                    'specification vspec file. This schema generator converts '
                    'not only from one format into the other, but enriches'
                    ' the GraphQL schema with features such as min and max '
                    'ranges, authorizations and further more. Please read '
                    'the brief descriptions of the individual commands to '
                    'find out more.',
    )

    parser.add_argument(
        'vspec_file',
        help='The root vehicle specification file to parse.',
        type=str,
    )

    parser.add_argument(
        '--output',
        '-o',
        help='The GraphQL schema output file.',
        default='resources/schema.graphql',
        type=str,
        nargs='?',
    )

    parser.add_argument(
        '--layer',
        help='The root deployment file that describes the layer that is taken '
             'into account when generating the GraphQL schema. At the moment '
             'the deployment file is used for filtering VSS leaves, '
             'determining which actuators have mutations and which VSS leaves '
             'are lists. Using this option, the parser will only generate the '
             'GraphQL schema out of the intersecting attributes, that occur '
             'in both the VSS vspec file and the layer deployment file. The '
             'remaining VSS data points are not taken into account in the '
             'GraphQL schema generation.',
        metavar='filename.depl',
    )

    parser.add_argument(
        '-I',
        help='Add include directory to search for included vspec files. '
             'Can be used multiple times. ',
        metavar='include_dir',
        action='append',
        dest='dirs',
    )

    parser.add_argument(
        '--regex-match',
        help='Consider only nodes with node.qualified_names("_") (name with '
             'full path separated by "_") that match this regex pattern.',
        metavar='regex_expression',
    )

    parser.add_argument(
        '--regex-filter',
        help='Do not consider nodes (and its children) with '
             'node.qualified_names("_") that match this regex pattern.',
        metavar='regex_expression',
    )

    parser.add_argument(
        '--custom-scalars',
        help='Generate custom scalars in the GraphQL schema out of data types '
             'mentioned in the VSS vspec file.',
        action='store_true',
    )

    parser.add_argument(
        '--permission-directive',
        help='Generate authorization directive by adding hasPermission '
             'declaration to the GraphqL schema.',
        action='store_true',
    )

    parser.add_argument(
        '--range-directive',
        help='Generate range directive by adding min and max declaration for '
             'VSS data points with min/max declarations in the vspec file.',
        action='store_true',
    )

    parser.add_argument(
        '--enums',
        help='Generate enums in the GraphQL schema based on VSS data points '
             'with enum declaration in the vspec file.',
        action='store_true',
    )

    parser.add_argument(
        '--subscription-delivery-interval',
        help='Generate delivery interval subscription parameter in the '
             'GraphQL schema file.',
        action='store_true',
    )

    return parser


def main(raw_args=None):
    parser = get_arg_parse()
    args = parser.parse_args(raw_args)

    # Always search current directory for include_file
    include_dirs = ['.']
    if args.dirs:
        include_dirs.extend(args.dirs)

    # Loading tree using vss-tools
    vss_root_node = load_tree(
        args.vspec_file, include_dirs, merge_private=True
    )

    # Creating regex filters
    filters = []
    if args.regex_match:
        filters.append(create_match_pattern(args.regex_match))
    if args.regex_filter:
        filters.append(create_filter_pattern(args.regex_filter))

    layer = None
    if args.layer:
        layer = Layer(args.layer)
        filters.append(create_layer_filter(layer))

    # Filtering
    vss_roots = list(VSSTreeFilter(
        [vss_root_node], filters
    ).filter_trees())

    # Sorting the children list on all nodes
    for r in vss_roots:
        sort_children(r)

    # Generating schema file
    with open(args.output, 'w') as schema_file:
        if layer:
            GraphQLSchemaVSSLayer(
                schema_file=schema_file, vss_roots=vss_roots, args=args,
                layer=layer,
            ).create_schema()
        else:
            GraphQLSchemaVSS(
                schema_file=schema_file, vss_roots=vss_roots, args=args,
            ).create_schema()


if __name__ == '__main__':
    main()
