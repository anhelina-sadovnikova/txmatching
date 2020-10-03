from dataclasses import dataclass
from typing import List, Optional

from txmatching.patients.patient_parameters import Centimeters, Kilograms
from txmatching.utils.enums import Sex


@dataclass
class DonorUploadDTO:
    # pylint: disable=too-many-instance-attributes
    medical_id: str
    blood_group: str
    HLA_typing: List[str]  # pylint: disable=invalid-name
    donor_type: str
    related_recipient_medical_id: Optional[str]
    sex: Optional[Sex]
    height: Optional[Centimeters]
    weight: Optional[Kilograms]
    YOB: Optional[int]  # pylint: disable=invalid-name
