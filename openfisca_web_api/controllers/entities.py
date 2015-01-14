# -*- coding: utf-8 -*-


# OpenFisca -- A versatile microsimulation software
# By: OpenFisca Team <contact@openfisca.fr>
#
# Copyright (C) 2011, 2012, 2013, 2014, 2015 OpenFisca Team
# https://github.com/openfisca
#
# This file is part of OpenFisca.
#
# OpenFisca is free software; you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
#
# OpenFisca is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.


"""Entities controller"""


import collections

from .. import contexts, model, wsgihelpers


@wsgihelpers.wsgify
def api1_entities(req):
    def build_entity_data(entity_class):
        entity_data = {
            'isPersonsEntity': entity_class.is_persons_entity,
            'label': entity_class.label,
            'nameKey': entity_class.name_key,
            }
        if hasattr(entity_class, 'roles_key'):
            entity_data.update({
                'maxCardinalityByRoleKey': entity_class.max_cardinality_by_role_key,
                'roles': entity_class.roles_key,
                'labelByRoleKey': entity_class.label_by_role_key,
                })
        return entity_data

    ctx = contexts.Ctx(req)
    headers = wsgihelpers.handle_cross_origin_resource_sharing(ctx)

    assert req.method == 'GET', req.method

    entities_class = model.tax_benefit_system.entity_class_by_key_plural.itervalues()
    data = collections.OrderedDict(sorted({
        entity_class.key_plural: build_entity_data(entity_class)
        for entity_class in entities_class
        }.iteritems()))
    return wsgihelpers.respond_json(ctx, data, headers = headers)