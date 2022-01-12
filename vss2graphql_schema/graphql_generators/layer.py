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

import os
from typing import Iterator, Tuple, Optional, Set

from .util import load_yaml


class Layer:
    '''
    Layer class to handle loading, standard Layer tree iterations and special
    variables that saves sets of key node names.
    '''
    yaml_tree: dict
    list_node_names: Set[str]
    write_node_names: Set[str]

    def __init__(self, file: str) -> None:
        with open(file) as layer_file:
            self.yaml_tree = load_yaml(layer_file, os.path.dirname(file))
        self.list_node_names = set(self.get_list_node_names())
        self.write_node_names = set(self.get_write_node_names())

    def iterate_qualified_names(
            self, entry: Optional[dict] = None, path: str = '', sep: str = '_'
    ) -> Iterator[str]:
        '''
        :param entry: Node to check, if none will get layer root
        :param path: Current node path
        :param sep: Separator of qualified name
        :return: Next layer qualified name
        '''
        entry = entry if entry else self.yaml_tree

        for k, v in entry.items():
            cur_name = path + sep + k if path else k
            if k == '_constants':
                v_elem = next(iter(v.values()))
                for p in v_elem.keys():
                    yield path + sep + p
            if k[0] != '_':
                if isinstance(v, dict):
                    for p in self.iterate_qualified_names(
                            entry=v, path=cur_name, sep=sep
                    ):
                        yield p
                elif isinstance(v, list):
                    for elem in v:
                        for p in self.iterate_qualified_names(
                                entry=elem, path=cur_name, sep=sep
                        ):
                            yield p
                else:
                    yield cur_name + str(v)

                yield cur_name

    def iterate_qualified_name_value(
            self, entry: Optional[dict] = None, path: str = None,
            sep: str = '_'
    ) -> Iterator[Tuple[str, dict]]:
        '''
        :param entry: Node to check, if none will get layer root
        :param path: Current node path
        :param sep: Separator of qualified name
        :return: Tuple with next layer qualified name and its value
        '''
        entry = entry if entry else self.yaml_tree

        for k, v in entry.items():
            cur_name = path + sep + k if path else k

            if k[0] != '_':
                if isinstance(v, dict):
                    for nk, p in self.iterate_qualified_name_value(
                            entry=v, path=cur_name, sep=sep
                    ):
                        yield nk, p
                elif isinstance(v, list):
                    for elem in v:
                        for nk, p in self.iterate_qualified_name_value(
                                entry=elem, path=cur_name, sep=sep
                        ):
                            yield nk, p
                else:
                    yield cur_name, v

                yield cur_name, v

    def get_list_node_names(self) -> Iterator[str]:
        '''
        :return: Next node name of lists on Layer
        '''
        for name, entry in self.iterate_qualified_name_value():
            if isinstance(entry, list):
                yield name
            elif (isinstance(entry, dict)
                  and '_constants' in entry):
                yield name

    def get_write_node_names(self) -> Iterator[str]:
        '''
        :return: Next node name of nodes with write on Layer
        '''
        for name, entry in self.iterate_qualified_name_value():
            if isinstance(entry, list):
                entry = entry[0]
            if isinstance(entry, dict):
                for child_name, d in entry.items():
                    if isinstance(d, dict) and Layer.has_write(d):
                        yield name
                        break

    @staticmethod
    def entry_has_franca_idl_write(entry: dict) -> bool:
        '''
        :param entry: Layer entry to consider (layer tree node)
        :return: True if entry a _francaIDL write description
        '''
        if '_francaIDL' in entry:
            if 'methods' in entry['_francaIDL']:
                return 'write' in entry['_francaIDL']['methods']
        return False

    @staticmethod
    def entry_has_custom_write(entry: dict) -> bool:
        '''
        :param entry: Layer entry to consider (layer tree node)
        :return: True if entry a _custom write description
        '''
        if '_custom' in entry:
            if 'methods' in entry['_custom']:
                return 'write' in entry['_custom']['methods']
        return False

    @staticmethod
    def has_dispatcher_write(entry: dict) -> bool:
        '''
        :param entry: Layer entry to consider (layer tree node)
        :return: True if entry a _dispatcher with a _francaIDL write
         description
        '''
        if '_dispatcher' in entry:
            if 'options' in entry['_dispatcher']:
                opts = entry['_dispatcher']['options']
                if isinstance(opts, list):
                    for o in opts:
                        if Layer.entry_has_franca_idl_write(o):
                            return True
        return False

    @staticmethod
    def has_write(entry: dict) -> bool:
        '''
        :param entry: Layer entry to consider (layer tree node)
        :return: True if entry a _dispatcher, _custom or a _francaIDL write
            description
        '''
        return (Layer.entry_has_franca_idl_write(entry)
                or Layer.has_dispatcher_write(entry)
                or Layer.entry_has_custom_write(entry))
