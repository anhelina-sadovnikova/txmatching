from dataclasses import dataclass, field
from typing import List, Optional

from txmatching.utils.blood_groups import BloodGroup
from txmatching.utils.enums import Country, Sex
from txmatching.utils.hla_system.hla_transformations import (
    get_compatibility_broad_codes, parse_code)

Kilograms = float
Centimeters = int


@dataclass
class HLAType:
    raw_code: str
    code: Optional[str] = None

    def __post_init__(self):
        if self.code is None:
            code = parse_code(self.raw_code)
            object.__setattr__(self, 'code', code)


@dataclass
class HLATyping:
    hla_types_list: List[HLAType] = field(default_factory=list)
    codes: Optional[List[str]] = None

    def __post_init__(self):
        if self.codes is None:
            codes = [hla_type.code for hla_type in self.hla_types_list]
            object.__setattr__(self, 'codes', codes)

    @property
    def compatibility_broad_resolution_codes(self) -> List[str]:
        return get_compatibility_broad_codes(self.codes)


@dataclass
class HLAAntibody:
    raw_code: str
    mfi: int
    cutoff: int
    code: Optional[str] = None

    def __post_init__(self):
        if self.code is None:
            code = parse_code(self.raw_code)
            object.__setattr__(self, 'code', code)


@dataclass
class HLAAntibodies:
    hla_antibodies_list: List[HLAAntibody] = field(default_factory=list)
    hla_codes_over_cutoff: List[str] = field(default_factory=list)

    def __init__(self, hla_antibodies_list: List[HLAAntibody] = None):
        if hla_antibodies_list is None:
            hla_antibodies_list = []
        object.__setattr__(self, 'hla_antibodies_list', hla_antibodies_list)
        hla_codes_over_cutoff = [hla_antibody.code for hla_antibody in hla_antibodies_list if
                                 hla_antibody.mfi >= hla_antibody.cutoff and hla_antibody.code]
        object.__setattr__(self, 'hla_codes_over_cutoff', hla_codes_over_cutoff)


@dataclass
class PatientParameters:
    blood_group: BloodGroup
    country_code: Country
    hla_typing: HLATyping = HLATyping()
    sex: Optional[Sex] = None
    height: Optional[Centimeters] = None
    weight: Optional[Kilograms] = None
    yob: Optional[int] = None
