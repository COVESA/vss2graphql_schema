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

from pkg_resources import resource_stream

from jinja2 import Environment, ChoiceLoader, FunctionLoader, FileSystemLoader

from vss2graphql_schema.graphql_generators.template_filters import all_filters

templates_dir = os.path.join(os.path.dirname(__file__), 'templates')


def load_template(
        name: str, module: str = 'vss2graphql_schema.graphql_generators',
        folder='templates'
) -> str:
    '''
    Load template from 'templates' folder in module specified
    :param name: Name of the template
    :param module: Module to search
    :param folder: Folder inside module with desired template
    :return: string with the template on it
    '''
    with resource_stream(module, os.path.join(folder, name)) as file:
        return file.read().decode('utf-8')


loader = ChoiceLoader([
    FunctionLoader(load_template),
    FileSystemLoader(templates_dir),
])


class Templates:
    '''
    Templates class to handle jinja templates, environment, filters and
     templates
    '''
    env = Environment(
        loader=loader,
        trim_blocks=True,
        lstrip_blocks=True,
        keep_trailing_newline=True,
    )
    # TODO: tests
    env.filters.update(all_filters)

    # keep sorted! -- do not break lines, it's easier to sort
    custom_scalar_close = env.get_template('custom_scalar_close.jinja')
    custom_scalar_entry = env.get_template('custom_scalar_entry.jinja')
    custom_scalar_open = env.get_template('custom_scalar_open.jinja')
    directive_close = env.get_template('directive_close.jinja')
    directive_entry = env.get_template('directive_entry.jinja')
    directive_open = env.get_template('directive_open.jinja')
    enum_close = env.get_template('enum_close.jinja')
    enum_entry = env.get_template('enum_entry.jinja')
    enum_open = env.get_template('enum_open.jinja')
    permission_enum = env.get_template('permission_enum.jinja')
    input_close = env.get_template('input_close.jinja')
    input_entry = env.get_template('input_entry.jinja')
    input_open = env.get_template('input_open.jinja')
    mutation_entry = env.get_template('mutation_entry.jinja')
    mutation_open = env.get_template('mutation_open.jinja')
    mutation_close = env.get_template('mutation_close.jinja')
    query_close = env.get_template('query_close.jinja')
    query_entry = env.get_template('query_entry.jinja')
    query_open = env.get_template('query_open.jinja')
    separator = env.get_template('separator.jinja')
    subscription_close = env.get_template('subscription_close.jinja')
    subscription_entry = env.get_template('subscription_entry.jinja')
    subscription_open = env.get_template('subscription_open.jinja')
    type_close = env.get_template('type_close.jinja')
    type_entry = env.get_template('type_entry.jinja')
    type_open = env.get_template('type_open.jinja')
