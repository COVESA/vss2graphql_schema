#!/bin/sh

# Copyright (C) 2021, Bayerische Motoren Werke Aktiengesellschaft (BMW AG),
#   Author: Alexander Domin (Alexander.Domin@bmw.de)
# Copyright (C) 2021, ProFUSION Sistemas e Soluções LTDA,
#   Author: Gustavo Barbieri (barbieri@profusion.mobi)
#   Author: Garbiel Fernandes (g7fernandes@profusion.mobi)
#   Author: Leandro Ferlin (leandroferlin@profusion.mobi)
#   Author: Leonardo Ramos (leo.ramos@profusion.mobi)
#
# SPDX-License-Identifier: MPL-2.0
#
# This Source Code Form is subject to the terms of the
# Mozilla Public License, v. 2.0. If a copy of the MPL was
# not distributed with this file, You can obtain one at
# http://mozilla.org/MPL/2.0/.

set -e

SELF=$(basename "$0")
HOOKS_DIR=$(dirname "$PWD"/"$0")
if [ -z "$GIT_DIR" ]; then
    GIT_DIR=$(git rev-parse --git-common-dir)
fi

for F in "$HOOKS_DIR"/*; do
    HOOK_NAME=$(basename "$F")
    if [ "$SELF" != "$HOOK_NAME" ] && [ -x "$F" ]; then
        echo "installing $F as $GIT_DIR/hooks/$HOOK_NAME"
        ln -sf "$F" "$GIT_DIR/hooks/$HOOK_NAME"
    fi
done
