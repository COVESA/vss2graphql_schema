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

from vspec.model.vsstree import VSSNode

from .vss_generator import VSSRootsGenerator
from ..emitters.subscription_emitter import SubscriptionEmitter
from ..model.directive_call import DirectiveCall
from ..model.field import Field
from ..model.parameter import Parameter
from ..util import (
    to_lower_camel_case, get_field_type, get_node_description,
    get_subscription_has_permission_directive
)


class SubscriptionGenerator(VSSRootsGenerator):
    '''
    Generates a GraphQL subscription for each root in VSS.
    '''
    has_permission_directive: bool

    def __init__(
            self, output: TextIO, vss_roots: Iterable[VSSNode],
            args: argparse.Namespace
    ) -> None:
        '''
        :param output: File to output GraphQL Subscription
        :param vss_roots: roots from VSS tree structure
        '''
        super(SubscriptionGenerator, self).__init__(
            output, 'subscription', SubscriptionEmitter, vss_roots, args
        )

    def _get_entries(self, roots: Iterable[VSSNode]) -> List[Field]:
        '''
        One field for each root.
        Changes the fields permissions to have 'DELIVERY_INTERVAL_1_SECOND' and
        'REALTIME'
        :param roots:
        :return: Fields from subscription
        '''
        subscriptions = []
        for r in roots:
            field = SubscriptionGenerator.field_from_vss_node(
                r, custom_scalars=self.args.custom_scalars,
                enums=self.args.enums,
                has_has_permission_directive=self.args.permission_directive,
                has_delivery_interval=self.args.subscription_delivery_interval
            )
            subscriptions.append(field)
        return subscriptions

    @staticmethod
    def field_from_vss_node(
            vss_node: VSSNode, custom_scalars: bool = False,
            enums: bool = False, has_has_permission_directive: bool = False,
            has_delivery_interval: bool = False,
    ) -> Field:
        field_name = to_lower_camel_case(vss_node.name)
        field_type = get_field_type(vss_node, custom_scalars, enums)
        description = get_node_description(vss_node)

        directives: List[DirectiveCall] = []
        parameters: List[Parameter] = []
        if has_delivery_interval:
            if has_has_permission_directive:
                parameters.append(Parameter(
                    'deliveryInterval', 'SubscriptionDeliveryInterval',
                    'DELIVERY_INTERVAL_5_SECONDS', is_required=True
                ))

                has_permission_directive = \
                    get_subscription_has_permission_directive(
                        vss_node, ['DELIVERY_INTERVAL_1_SECOND', 'REALTIME']
                    )
                if has_permission_directive:
                    directives.append(has_permission_directive)

        return Field(
            field_name, field_type, description,
            parameters, directives,
        )
