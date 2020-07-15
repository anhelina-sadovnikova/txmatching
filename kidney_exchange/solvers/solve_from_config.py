import dataclasses
from dataclasses import dataclass
from typing import List, Iterator, Optional, Iterable, Tuple

import numpy as np

from kidney_exchange.config.configuration import Configuration
from kidney_exchange.config.gives_superset_of_solutions import gives_superset_of_solutions
from kidney_exchange.database.db import db
from kidney_exchange.database.services.config_service import get_current_configuration, save_configuration_to_db, \
    get_config_models, config_model_to_configuration
from kidney_exchange.database.services.patient_service import medical_id_to_db_id, get_donors_recipients_from_db
from kidney_exchange.database.services.scorer_service import score_matrix_to_dto
from kidney_exchange.database.services.services_for_solve import get_pairing_result_for_config, \
    get_patients_for_pairing_result, \
    db_matching_to_matching
from kidney_exchange.database.sql_alchemy_schema import PairingResultPatientModel, PairingResultModel
from kidney_exchange.filters.filter_from_config import filter_from_config
from kidney_exchange.patients.donor import Donor
from kidney_exchange.patients.recipient import Recipient
from kidney_exchange.scorers.scorer_from_config import scorer_from_configuration
from kidney_exchange.solvers.matching.matching import Matching
from kidney_exchange.solvers.solver_from_config import solver_from_config


@dataclass
class SolverInputParameters:
    donors: List[Donor]
    recipients: List[Recipient]
    configuration: Configuration


@dataclass
class DonorRecipient:
    donor: int
    recipient: int


@dataclass
class CalculatedMatching:
    donors_recipients: List[DonorRecipient]


@dataclass
class CalculatedMatchings:
    matchings: List[CalculatedMatching]


def solve_from_db() -> Iterable[Matching]:
    donors, recipients = get_donors_recipients_from_db()

    current_configuration = get_current_configuration()
    current_config_matchings, score_matrix = solve_from_config(SolverInputParameters(
        donors=donors,
        recipients=recipients,
        configuration=current_configuration
    ))
    pairing_result_patients = [PairingResultPatientModel(patient_id=patient.db_id) for patient in donors + recipients]
    current_config_matchings_model = dataclasses.asdict(
        current_config_matchings_to_model(current_config_matchings)
    )

    config_id = save_configuration_to_db(current_configuration)
    pairing_result_model = PairingResultModel(
        patients=pairing_result_patients,
        score_matrix=score_matrix_to_dto(score_matrix),
        calculated_matchings=current_config_matchings_model,
        config_id=config_id,
        valid=True
    )
    db.session.add(pairing_result_model)
    db.session.commit()

    return current_config_matchings


def current_config_matchings_to_model(config_matchings: Iterable[Matching]) -> CalculatedMatchings:
    return CalculatedMatchings([
        CalculatedMatching([
            DonorRecipient(
                medical_id_to_db_id(donor.medical_id),
                medical_id_to_db_id(recipient.medical_id)
            ) for donor, recipient in final_solution.donor_recipient_list
        ]

        ) for final_solution in config_matchings
    ])


def solve_from_config(params: SolverInputParameters) -> Tuple[Iterable[Matching], np.array]:
    scorer = scorer_from_configuration(params.configuration)
    solver = solver_from_config(params.configuration)
    matchings_in_db = load_matchings_from_database(params)
    score_matrix = scorer.get_score_matrix(
        params.donors, params.recipients
    )
    if matchings_in_db is not None:
        all_solutions = matchings_in_db
    else:
        all_solutions = solver.solve(params.donors, params.recipients, score_matrix)

    matching_filter = filter_from_config(params.configuration)
    matchings_filtered = filter(matching_filter.keep, all_solutions)
    return list(matchings_filtered), score_matrix


def load_matchings_from_database(exchange_parameters: SolverInputParameters) -> Optional[Iterator[Matching]]:
    current_config = exchange_parameters.configuration

    compatible_config_models = list()
    for config_model in get_config_models():
        config_from_model = config_model_to_configuration(config_model)
        if gives_superset_of_solutions(less_strict=config_from_model,
                                       more_strict=current_config):
            compatible_config_models.append(config_model)

    current_patient_ids = {medical_id_to_db_id(patient.medical_id) for patient in
                           exchange_parameters.donors + exchange_parameters.recipients}

    for compatible_config in compatible_config_models:
        for pairing_result in get_pairing_result_for_config(compatible_config.id):
            compatible_config_patient_ids = {p.patient_id for p in get_patients_for_pairing_result(pairing_result.id)}
            if compatible_config_patient_ids == current_patient_ids:
                return db_matching_to_matching(pairing_result.calculated_matchings)

    return None


if __name__ == "__main__":
    config = Configuration()
    solutions, score_matrix = solve_from_config(params=SolverInputParameters(
        donors=list(),
        recipients=list(),
        configuration=config
    ))
    print(list(solutions))