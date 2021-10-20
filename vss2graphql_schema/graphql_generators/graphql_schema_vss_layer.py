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
from typing import TextIO, Iterable

from vspec.model.vsstree import VSSNode

from .layer import Layer
from .layer_generators.input_layer_generator import InputLayerGenerator
from .layer_generators.mutation_layer_generator import (
    MutationLayerGenerator
)
from .layer_generators.type_layer_generator import TypeLayerGenerator
from .vss_generators.custom_scalars_generator import CustomScalarsGenerator
from .vss_generators.directive_generator import DirectiveGenerator
from .vss_generators.enum_generator import EnumGenerator
from .vss_generators.query_generator import QueryGenerator
from .vss_generators.subscriptions_generator import SubscriptionGenerator


class GraphQLSchemaVSSLayer:
    '''
    Generates GraphQL Schema based on VSS. (See README.md to more details)
    '''
    _schema_file: TextIO
    vss_roots: Iterable[VSSNode]
    args: argparse.Namespace
    layer: Layer

    def __init__(
            self, schema_file: TextIO, vss_roots: Iterable[VSSNode],
            args: argparse.Namespace, layer: Layer
    ) -> None:
        '''
        :param schema_file: File to receive GraphQL Schema
        :param vss_roots: Roots from VSS tree structure
        :param args: Arguments from argparse in standard call
        :param layer: Layer class with its structure
        '''
        self._schema_file = schema_file
        self.vss_roots = vss_roots
        self.args = args
        self.layer = layer

    def create_schema(self) -> None:
        '''
        Orchestrate GraphQL schema generation
        :return: None
        '''
        DirectiveGenerator(
            self._schema_file, self.args,
        ).generate()

        if self.args.custom_scalars:
            CustomScalarsGenerator(
                self._schema_file, self.args,
            ).generate()

        QueryGenerator(
            self._schema_file, self.vss_roots, self.args,
        ).generate()

        SubscriptionGenerator(
            self._schema_file, self.vss_roots, self.args,
        ).generate(extra_vars={
            'include_delivery_interval':
                self.args.subscription_delivery_interval
        })

        MutationLayerGenerator(
            self._schema_file, self.vss_roots, self.args, self.layer
        ).generate()

        InputLayerGenerator(
            self._schema_file, self.vss_roots, self.args, self.layer
        ).generate()

        TypeLayerGenerator(
            self._schema_file, self.vss_roots, self.args, self.layer
        ).generate()

        if self.args.enums:
            EnumGenerator(
                self._schema_file, self.vss_roots, self.args,
            ).generate()
