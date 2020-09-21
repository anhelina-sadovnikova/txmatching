from typing import List

from txmatching.configuration.configuration import Configuration
from txmatching.filters.filter_base import FilterBase
from txmatching.solvers.matching.matching import Matching
from txmatching.solvers.matching.transplant_cycle import TransplantCycle
from txmatching.solvers.matching.transplant_sequence import TransplantSequence


class FilterDefault(FilterBase):
    @classmethod
    def from_config(cls, configuration: Configuration) -> 'FilterBase':
        return FilterDefault(max_cycle_length=configuration.max_cycle_length,
                             max_sequence_length=configuration.max_sequence_length,
                             max_number_of_distinct_countries_in_round=
                             configuration.max_number_of_distinct_countries_in_round,
                             required_patient_db_ids=configuration.required_patient_db_ids
                             )

    def __init__(self, max_cycle_length: int,
                 max_sequence_length: int,
                 max_number_of_distinct_countries_in_round: int,
                 required_patient_db_ids: List[int]):
        self._max_cycle_length = max_cycle_length
        self._max_sequence_length = max_sequence_length
        self._max_number_of_distinct_countries_in_round = max_number_of_distinct_countries_in_round
        self._required_patients = required_patient_db_ids

    def keep(self, matching: Matching) -> bool:
        sequences = matching.get_sequences()
        cycles = matching.get_cycles()

        if max(cycles, key=lambda cycle: cycle.length,
               default=TransplantCycle([])).length > self._max_cycle_length:
            return False

        if max(sequences, key=lambda sequence: sequence.length,
               default=TransplantSequence([])).length > self._max_sequence_length:
            return False

        for patient_db_id in self._required_patients:
            if not any([transplant_round.contains_patient_db_id(patient_db_id) for transplant_round in
                        sequences + cycles]):
                return False

        return True
