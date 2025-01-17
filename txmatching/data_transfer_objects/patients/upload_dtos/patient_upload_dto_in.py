from dataclasses import dataclass
from typing import List

from txmatching.data_transfer_objects.patients.upload_dtos.donor_upload_dto import \
    DonorUploadDTO
from txmatching.data_transfer_objects.patients.upload_dtos.recipient_upload_dto import \
    RecipientUploadDTO
from txmatching.utils.country_enum import Country


@dataclass
class PatientUploadDTOIn:
    country: Country
    txm_event_name: str
    donors: List[DonorUploadDTO]
    recipients: List[RecipientUploadDTO]
    add_to_existing_patients: bool = False
