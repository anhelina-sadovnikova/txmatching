from dataclasses import dataclass
from typing import List, Optional

from txmatching.data_transfer_objects.patients.patient_base_dto import \
    PatientBaseDTO
from txmatching.patients.patient_parameters import Centimeters, Kilograms
from txmatching.utils.blood_groups import BloodGroup
from txmatching.utils.enums import Sex


@dataclass(kw_only=True)
class DonorUploadDTO(PatientBaseDTO):
    # pylint: disable=too-many-instance-attributes
    medical_id: str
    blood_group: BloodGroup
    hla_typing: List[str]
    donor_type: str
    related_recipient_medical_id: Optional[str]
    sex: Optional[Sex] = None
    height: Optional[Centimeters] = None
    weight: Optional[Kilograms] = None
    year_of_birth: Optional[int] = None
    note: str = ''
    internal_medical_id: Optional[str] = None
