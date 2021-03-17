import unittest

from tests.patients.test_patient_parameters import (donor_parameters_Joe,
                                                    recipient_parameters_Jack)
from tests.test_utilities.hla_preparation_utils import (get_hla_type,
                                                        get_hla_typing)
from txmatching.patients.patient import Donor, Recipient
from txmatching.patients.patient_parameters import PatientParameters
from txmatching.scorers.high_res_hla_additive_scorer import \
    HighResHLAAdditiveScorer
from txmatching.scorers.split_hla_additive_scorer import SplitHLAAdditiveScorer
from txmatching.utils.blood_groups import BloodGroup
from txmatching.utils.country_enum import Country
from txmatching.utils.enums import HLAGroup, MatchTypes
from txmatching.utils.hla_system.compatibility_index import (
    DetailedCompatibilityIndexForHLAGroup, HLAMatch,
    get_detailed_compatibility_index)


class TestHlaScorer(unittest.TestCase):

    def test_get_genotype(self):
        calculated_detailed_score = get_detailed_compatibility_index(donor_parameters_Joe.hla_typing,
                                                                     recipient_parameters_Jack.hla_typing)

        expected = [
            DetailedCompatibilityIndexForHLAGroup(
                hla_group=HLAGroup.A,
                donor_matches=[HLAMatch(get_hla_type('A23'), MatchTypes.BROAD),
                               HLAMatch(get_hla_type('A26'), MatchTypes.NONE)],
                recipient_matches=[HLAMatch(get_hla_type('A9'), MatchTypes.BROAD),
                                   HLAMatch(get_hla_type('A30'), MatchTypes.NONE)],
                group_compatibility_index=1.0),
            DetailedCompatibilityIndexForHLAGroup(
                hla_group=HLAGroup.B,
                donor_matches=[HLAMatch(get_hla_type('B62'), MatchTypes.BROAD),
                               HLAMatch(get_hla_type('B38'), MatchTypes.NONE)],
                recipient_matches=[HLAMatch(get_hla_type('B77'), MatchTypes.BROAD),
                                   HLAMatch(get_hla_type('B14'), MatchTypes.NONE)],
                group_compatibility_index=3.0),
            DetailedCompatibilityIndexForHLAGroup(
                hla_group=HLAGroup.DRB1,
                donor_matches=[HLAMatch(get_hla_type('DR4'), MatchTypes.SPLIT),
                               HLAMatch(get_hla_type('DR11'), MatchTypes.SPLIT)],
                recipient_matches=[HLAMatch(get_hla_type('DR4'), MatchTypes.SPLIT),
                                   HLAMatch(get_hla_type('DR11'), MatchTypes.SPLIT)],
                group_compatibility_index=18.0),
            DetailedCompatibilityIndexForHLAGroup(hla_group=HLAGroup.Other,
                                                  donor_matches=[
                                                      HLAMatch(hla_type=get_hla_type('DR52'),
                                                               match_type=MatchTypes.NONE),
                                                      HLAMatch(hla_type=get_hla_type('DR53'),
                                                               match_type=MatchTypes.NONE),
                                                      HLAMatch(hla_type=get_hla_type('DQ7'),
                                                               match_type=MatchTypes.NONE),
                                                      HLAMatch(hla_type=get_hla_type('DQ8'),
                                                               match_type=MatchTypes.NONE),
                                                      HLAMatch(hla_type=get_hla_type('DP2'),
                                                               match_type=MatchTypes.NONE),
                                                      HLAMatch(hla_type=get_hla_type('DP10'),
                                                               match_type=MatchTypes.NONE),
                                                      HLAMatch(hla_type=get_hla_type('CW9'),
                                                               match_type=MatchTypes.NONE),
                                                      HLAMatch(hla_type=get_hla_type('CW12'),
                                                               match_type=MatchTypes.NONE)],
                                                  recipient_matches=[], group_compatibility_index=0.0)

        ]
        self.maxDiff = None
        for expected_result, actual_result in zip(expected, calculated_detailed_score):
            self.assertSetEqual(set(expected_result.donor_matches), set(actual_result.donor_matches))
            self.assertSetEqual(set(expected_result.recipient_matches), set(actual_result.recipient_matches))

    def test_scorers_on_some_patients(self):
        split_scorer = SplitHLAAdditiveScorer()
        high_res_scorer = HighResHLAAdditiveScorer()
        donor = Donor(
            db_id=1,
            medical_id='donor',
            parameters=donor_parameters_Joe
        )
        recipient = Recipient(
            db_id=1,
            acceptable_blood_groups=[],
            related_donor_db_id=1,
            medical_id='recipient',
            parameters=recipient_parameters_Jack
        )
        original_donor = Donor(
            db_id=2,
            medical_id='original_donor',
            related_recipient_db_id=1,
            parameters=PatientParameters(
                blood_group=BloodGroup.A,
                country_code=Country.CZE,
                hla_typing=get_hla_typing(
                    ['A1',
                     'A9',
                     'B7',
                     'B37',
                     'DR11',
                     'DR15',
                     'DR52',
                     'DR51',
                     'DQ7',
                     'DQ6']
                )
            )
        )

        # A9 - BROAD +1
        # B77 - BROAD +3
        # DR4, DR11 - SPLIT +9 +9
        self.assertEqual(22,
                         split_scorer.score_transplant(donor=donor, recipient=recipient, original_donor=original_donor))

        # A9 - BROAD +1
        # B77 - BROAD +1
        # DR4, DR11 - SPLIT +2 +2
        self.assertEqual(6, high_res_scorer.score_transplant(donor=donor, recipient=recipient,
                                                             original_donor=original_donor))
