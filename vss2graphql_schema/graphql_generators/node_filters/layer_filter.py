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

from typing import Callable

from ..layer import Layer


def create_layer_filter(
        layer: Layer
) -> Callable[[str], bool]:
    '''
    :param layer: Layer class to get node qualified names
    :return: A filter that returns True if the node is on layer and returns
     False otherwise
    '''
    nodes_to_include = set(layer.iterate_qualified_names())
    return lambda x: x in nodes_to_include
