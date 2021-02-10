import { RecipientGenerated, RecipientRequirementsGenerated } from '../generated';
import { Recipient, RecipientRequirements } from '../model';
import { parsePatient } from './patient.parsers';
import { parseAntibodiesPerGroup, parseAntibody } from './hla.parsers';

export const parseRecipient = (data: RecipientGenerated): Recipient => {
  return {
    ...parsePatient(data),
    acceptable_blood_groups: data.acceptable_blood_groups ?? [],
    // TODO: https://github.com/mild-blue/txmatching/issues/401 create hla_antibodies model
    hla_antibodies: {
      hla_antibodies_list: data.hla_antibodies?.hla_antibodies_list.map(parseAntibody) ?? [],
      hla_antibodies_per_groups: data.hla_antibodies?.hla_antibodies_per_groups.map(parseAntibodiesPerGroup) ?? []
    },
    recipient_requirements: data.recipient_requirements && parseRecipientRequirements(data.recipient_requirements),
    related_donor_db_id: data.related_donor_db_id,
  };
};

export const parseRecipientRequirements = (data: RecipientRequirementsGenerated): RecipientRequirements => {
  const {
    require_better_match_in_compatibility_index,
    require_better_match_in_compatibility_index_or_blood_group,
    require_compatible_blood_group
  } = data;

  return {
    require_better_match_in_compatibility_index,
    require_better_match_in_compatibility_index_or_blood_group,
    require_compatible_blood_group
  };
};