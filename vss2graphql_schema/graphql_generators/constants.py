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

from typing import Dict, Set

from vspec.model.constants import VSSDataType, VSSType

GQL_SCALARS_MAPPING: Dict[VSSDataType, str] = {
    VSSDataType.INT8: 'Int',
    VSSDataType.UINT8: 'Int',
    VSSDataType.INT16: 'Int',
    VSSDataType.UINT16: 'Int',
    VSSDataType.INT32: 'Int',
    VSSDataType.UINT32: 'Int',
    VSSDataType.INT64: 'String',
    VSSDataType.UINT64: 'String',
    VSSDataType.FLOAT: 'Float',
    VSSDataType.DOUBLE: 'Float',
    VSSDataType.BOOLEAN: 'Boolean',
    VSSDataType.STRING: 'String',
}

GQL_ARRAY_MAPPING: Dict[VSSDataType, str] = {
    VSSDataType.INT8_ARRAY: '[Int]',
    VSSDataType.UINT8_ARRAY: '[Int]',
    VSSDataType.INT16_ARRAY: '[Int]',
    VSSDataType.UINT16_ARRAY: '[Int]',
    VSSDataType.INT32_ARRAY: '[Int]',
    VSSDataType.UINT32_ARRAY: '[Int]',
    VSSDataType.INT64_ARRAY: '[String]',
    VSSDataType.UINT64_ARRAY: '[String]',
    VSSDataType.FLOAT_ARRAY: '[Float]',
    VSSDataType.DOUBLE_ARRAY: '[Float]',
    VSSDataType.BOOLEAN_ARRAY: '[Boolean]',
    VSSDataType.STRING_ARRAY: '[String]',
}

VSS_CUSTOM_SCALARS_MAPPING: Dict[VSSDataType, str] = {
    VSSDataType.INT8: 'Int8',
    VSSDataType.UINT8: 'UInt8',
    VSSDataType.INT16: 'Int16',
    VSSDataType.UINT16: 'UInt16',
    VSSDataType.INT32: 'Int32',
    VSSDataType.UINT32: 'UInt32',
    VSSDataType.INT64: 'Int64',
    VSSDataType.UINT64: 'UInt64',
}

VSS_CUSTOM_ARRAY_MAPPING: Dict[VSSDataType, str] = {
    VSSDataType.INT8_ARRAY: '[Int8]',
    VSSDataType.UINT8_ARRAY: '[UInt8]',
    VSSDataType.INT16_ARRAY: '[Int16]',
    VSSDataType.UINT16_ARRAY: '[UInt16]',
    VSSDataType.INT32_ARRAY: '[Int32]',
    VSSDataType.UINT32_ARRAY: '[UInt32]',
    VSSDataType.INT64_ARRAY: '[Int64]',
    VSSDataType.UINT64_ARRAY: '[UInt64]',
}

VSS_GQL_TYPE_MAPPING = {
    **GQL_ARRAY_MAPPING,
    **GQL_SCALARS_MAPPING,
}

VSS_GQL_CUSTOM_TYPE_MAPPING: Dict[VSSDataType, str] = {
    **VSS_GQL_TYPE_MAPPING,
    **VSS_CUSTOM_SCALARS_MAPPING,
    **VSS_CUSTOM_ARRAY_MAPPING,
}

VSS_BRANCH_TYPES = {VSSType.BRANCH, VSSType.RBRANCH}

VSS_LEAF_TYPES = {
    VSSType.ATTRIBUTE, VSSType.SENSOR, VSSType.ACTUATOR, VSSType.ELEMENT
}

VSS_UNSIGNED_INTEGER_TYPES: Set[VSSDataType] = {
    VSSDataType.UINT8,
    VSSDataType.UINT16,
    VSSDataType.UINT32,
    VSSDataType.UINT64
}

VSS_INTEGER_TYPES: Set[VSSDataType] = {
    *VSS_UNSIGNED_INTEGER_TYPES,
    VSSDataType.INT8,
    VSSDataType.INT16,
    VSSDataType.INT32,
    VSSDataType.INT64
}
