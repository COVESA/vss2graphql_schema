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
from abc import ABC, abstractmethod
from typing import (
    Generic, Iterable, Optional, Mapping, List, TextIO, Type, Iterator, Any
)

from anytree import LevelOrderIter

from vspec import VSSNode

from ..emitters.common_emitter import TEntry, CommonEmitter
from ..common_generator import CommonGenerator


class VSSGenerator(CommonGenerator, Generic[TEntry], ABC):
    '''
    Generator specialized in VSSNodes.
    Default iterator that yields every node in DFS order.
    Its 'generate' method writes the separator and calls 'self.emitter' for
    each node, using 'self._get_entries' and 'self._get_extra_vars_from_node'
    to get needed info necessary to generate.
    '''
    vss_roots: Iterable[VSSNode]

    def __init__(
            self, output: TextIO, name: str, emitter: Type[CommonEmitter],
            vss_roots: Iterable[VSSNode], args: argparse.Namespace
    ) -> None:

        super().__init__(output, name, emitter, args)
        self.vss_roots = vss_roots

    @abstractmethod
    def __iter__(self) -> Iterator[VSSNode]:
        raise NotImplementedError()

    def generate(self, extra_vars: Optional[Mapping[str, str]] = None) -> None:
        '''
        Iterates with default iterator, get entries and emits for each node.
        :param extra_vars: Extra variables to be sent to emitter
        :return: None
        '''
        if extra_vars is None:
            extra_vars = {}

        self.emit_separator()

        for node in self:
            entries: List[TEntry] = self._get_entries(node)
            if len(entries) > 0:
                gen = self.emitter(self.output, self.name, entries)
                node_extra_vars = self._get_extra_vars_from_node(node)
                gen.emit_all(extra_vars={
                    **extra_vars,
                    **node_extra_vars,
                })

    def _get_extra_vars_from_node(self, node: VSSNode) -> Mapping[str, Any]:
        '''
        Get variables from node
        :param node: VSSNode
        :return: Variables from node in Mapping form
        '''
        return {}

    @abstractmethod
    def _get_entries(self, node: VSSNode) -> List[TEntry]:
        '''
        Get entries from node to be emitted
        :param node:
        :return: List of entries
        '''
        raise NotImplementedError()


class VSSLeafGenerator(VSSGenerator, ABC):
    '''
    VSSGenerator with standard iterator returning all nodes in DFS order
    '''
    def __init__(
            self, output: TextIO, name: str, emitter: Type[CommonEmitter],
            vss_roots: Iterable[VSSNode], args: argparse.Namespace
    ) -> None:
        super().__init__(output, name, emitter, vss_roots, args)

    def __iter__(self) -> Iterator[VSSNode]:
        '''
        Default iteration for vss is a DFS in vss tree
        '''
        for root in self.vss_roots:
            for node in LevelOrderIter(root):
                yield node


class VSSRootsGenerator(VSSGenerator, ABC):
    '''
    VSSGenerator with iterator returning
    '''
    def __init__(
            self, output: TextIO, name: str, emitter: Type[CommonEmitter],
            vss_roots: Iterable[VSSNode], args: argparse.Namespace
    ) -> None:
        super().__init__(output, name, emitter, vss_roots, args)

    def __iter__(self) -> Iterator[Iterable[VSSNode]]:
        '''
        Default iteration for vss is a DFS in vss tree
        '''
        yield self.vss_roots
