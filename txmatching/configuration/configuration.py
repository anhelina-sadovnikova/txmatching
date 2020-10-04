from dataclasses import dataclass, field
from typing import List

from txmatching.configuration.subclasses import (ForbiddenCountryCombination,
                                                 ManualDonorRecipientScore,
                                                 PatientDbId)
from txmatching.utils.enums import Country

DEFAULT_FORBIDDEN_COUNTRY_LIST = [ForbiddenCountryCombination(Country.AUT, Country.IL),
                                  ForbiddenCountryCombination(Country.IL, Country.AUT)]


# pylint: disable=too-many-instance-attributes
# I think it is reasonable to have many attributes here

@dataclass
class Configuration:
    """
    Attributes:
        minimum_total_score: Minimum total score (compatibility index + blood group bonus) that is required for
        a transplant to be possible
        use_binary_scoring: If all the conditions above are satisfied, then use just 1 for possible transplant
        and -inf for impossible
    manual_donor_recipient_scores: Manual setting of score for tuple of recipient and donor
    """
    scorer_constructor_name: str = 'HLAAdditiveScorer'
    solver_constructor_name: str = 'AllSolutionsSolver'
    require_compatible_blood_group: bool = False
    minimum_total_score: float = 0.0
    maximum_total_score: float = 27.0
    require_better_match_in_compatibility_index: bool = False
    require_better_match_in_compatibility_index_or_blood_group: bool = False
    blood_group_compatibility_bonus: float = 0.0
    use_binary_scoring: bool = False
    max_cycle_length: int = 100
    max_sequence_length: int = 100
    max_number_of_distinct_countries_in_round: int = 100
    required_patient_db_ids: List[PatientDbId] = field(default_factory=list)
    use_split_resolution: bool = False
    forbidden_country_combinations: List[ForbiddenCountryCombination] = field(
        default_factory=lambda: DEFAULT_FORBIDDEN_COUNTRY_LIST)
    manual_donor_recipient_scores: List[ManualDonorRecipientScore] = field(default_factory=list)
    max_matchings_to_show_to_viewer: int = 10