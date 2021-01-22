from flask_restx import fields

from txmatching.utils.enums import HLA_GROUPS_NAMES_WITH_OTHER, HLAGroup
from txmatching.web.api.namespaces import patient_api

HLA_TYPES_PER_GROUPS_EXAMPLE = [
    {'hla_group': HLAGroup.A.name,
     'hla_types': [{'code': 'A1', 'raw_code': 'A1'}]},
    {'hla_group': HLAGroup.B.name,
     'hla_types': [{'code': 'B38', 'raw_code': 'B38'}]},
    {'hla_group': HLAGroup.DRB1.name,
     'hla_types': [{'code': 'DR7', 'raw_code': 'DR7'}]},
    {'hla_group': HLAGroup.Other.name,
     'hla_types': [{'code': 'CW4', 'raw_code': 'CW4'}]}
]
HLA_ANTIBODIES_PER_GROUPS_EXAMPLE = [
    {'hla_group': HLAGroup.A.name,
     'hla_antibody_list': [{'code': 'A1', 'raw_code': 'A1', 'mfi': 0, 'cutoff': 0}]},
    {'hla_group': HLAGroup.B.name,
     'hla_antibody_list': [{'code': 'B38', 'raw_code': 'B38', 'mfi': 10, 'cutoff': 0}]},
    {'hla_group': HLAGroup.DRB1.name,
     'hla_antibody_list': [{'code': 'DR7', 'raw_code': 'DR7', 'mfi': 0, 'cutoff': 300}]},
    {'hla_group': HLAGroup.Other.name,
     'hla_antibody_list': [{'code': 'CW4', 'raw_code': 'CW4', 'mfi': 500, 'cutoff': 500}]}
]
EXAMPLE_HLA_TYPING = {'hla_types_list': [{'raw_code': 'A*01:02'},
                                         {'raw_code': 'B7'},
                                         {'raw_code': 'DR11'}]}

HLAType = patient_api.model('HlaType', {
    'code': fields.String(required=False),
    'raw_code': fields.String(required=True),
})

HLAAntibody = patient_api.model('HlaAntibody', {
    'raw_code': fields.String(required=True),
    'mfi': fields.Integer(required=True),
    'cutoff': fields.Integer(required=True),
    'code': fields.String(required=False)
})

HlaPerGroup = patient_api.model('HlaCodesInGroups', {
    'hla_group': fields.String(required=True, enum=[group.name for group in HLA_GROUPS_NAMES_WITH_OTHER]),
    'hla_types': fields.List(required=True, cls_or_instance=fields.Nested(HLAType))
})

HLATyping = patient_api.model('HlaTyping', {
    'hla_types_list': fields.List(required=True, cls_or_instance=fields.Nested(HLAType)),
    'hla_per_groups': fields.List(required=True,
                                  description='hla types split to hla groups',
                                  example=HLA_TYPES_PER_GROUPS_EXAMPLE,
                                  cls_or_instance=fields.Nested(HlaPerGroup)),
})

AntibodiesPerGroup = patient_api.model('AntibodiesPerGroup', {
    'hla_group': fields.String(required=True, enum=[group.name for group in HLA_GROUPS_NAMES_WITH_OTHER]),
    'hla_antibody_list': fields.List(required=True, cls_or_instance=fields.Nested(HLAAntibody))
})

HLAAntibodies = patient_api.model('HlaAntibodies', {
    'hla_antibodies_list': fields.List(required=True, cls_or_instance=fields.Nested(HLAAntibody)),
    'hla_antibodies_per_groups': fields.List(required=True,
                                             description='hla antibodies split to hla groups',
                                             example=HLA_ANTIBODIES_PER_GROUPS_EXAMPLE,
                                             cls_or_instance=fields.Nested(AntibodiesPerGroup)),
})