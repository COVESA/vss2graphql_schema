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

from typing import Optional, Iterable, Callable, Iterator

from vspec.model.vsstree import VSSNode

from ..constants import VSS_LEAF_TYPES


class VSSTreeFilter:
    '''
    A Class to handle filtering of VSS nodes. It receives a list of filters and
    has a method filter_trees to remove nodes based on them
    :param roots: VSS root node
    :param filters: A list of filters (Functions that receive a node name and
    returns if that node is allowed or not)
    '''
    roots: Iterable[VSSNode]
    filters: Iterable[Callable[[str], bool]]

    def __init__(
            self, roots: Iterable[VSSNode],
            filters: Optional[Iterable[Callable[[str], bool]]] = None,
    ) -> None:
        self.roots = roots
        self.filters = filters if filters else ()

    def filter_trees(self) -> Iterator[VSSNode]:
        '''
        Filter the VSS tree and return the roots allowed by the filters
        :return: Next allowed root and with its children filtered
        '''
        for root in self.roots:
            filtered_node = self._filter_node(root)
            if filtered_node:
                yield filtered_node

    def _filter_node(self, node) -> Optional[VSSNode]:
        if self._allowed(node):
            node.children = [x for x in node.children if self._filter_node(x)]
            if node.type in VSS_LEAF_TYPES or len(node.children) > 0:
                return node
        return None

    def _allowed(self, node: VSSNode) -> bool:
        for f in self.filters:
            if not f(node.qualified_name('_')):
                return False
        return True
