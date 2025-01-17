import { DonorEditable } from '../../model/DonorEditable';
import { DonorInputGenerated, DonorModelToUpdateGenerated, DonorTypeGenerated } from '../../generated';
import { fromBloodGroup, fromPatientEditableToUpdateGenerated, fromSex } from './patient.parsers';
import { DonorType } from '@app/model';

/* Used for updating donor */
export const fromDonorEditableToUpdateGenerated = ( donor: DonorEditable, donorId: number, donorUpdateId: number ): DonorModelToUpdateGenerated => {
  return {
    ...fromPatientEditableToUpdateGenerated(donor, donorId, donorUpdateId),
    active: donor.active
  };
};

/* Used for creating donor */
// TODO: share logic with recipient
export const fromDonorEditableToInputGenerated = ( donor: DonorEditable ): DonorInputGenerated => {
  return {
    medical_id: donor.medicalId,
    blood_group: fromBloodGroup(donor.bloodGroup),
    hla_typing: donor.antigens.map(antigen => antigen.rawCode),
    donor_type: fromDonorType(donor.type),
    sex: donor.sex ? fromSex(donor.sex) : undefined,
    height: donor.height ? +donor.height : undefined,
    weight: donor.weight ? +donor.weight : undefined,
    year_of_birth: donor.yearOfBirth ? +donor.yearOfBirth : undefined,
    note: donor.note
  };
};

export const fromDonorType = ( donorType: DonorType ): DonorTypeGenerated => {
  switch (donorType) {
    case DonorType.DONOR: return DonorTypeGenerated.Donor;
    case DonorType.BRIDGING_DONOR: return DonorTypeGenerated.BridgingDonor;
    case DonorType.NON_DIRECTED: return DonorTypeGenerated.NonDirected;
    default: throw new Error(`Parsing from donor type ${donorType} not implemented`);
  }
};
