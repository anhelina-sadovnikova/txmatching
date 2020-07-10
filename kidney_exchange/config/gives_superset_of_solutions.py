from kidney_exchange.config.configuration import Configuration
from kidney_exchange.scorers.hla_additive_scorer import HLAAdditiveScorer
from kidney_exchange.solvers.all_solutions_solver import AllSolutionsSolver


def _check_if_config_is_supported(configuration: Configuration):
    if configuration.solver_constructor_name != AllSolutionsSolver.__name__ \
            and configuration.scorer_constructor_name != HLAAdditiveScorer.__name__:
        raise ValueError(f"Unsupported combination "
                         f"({configuration.scorer_constructor_name}, {configuration.solver_constructor_name}) "
                         f"of (scorer, solver)")


def gives_superset_of_solutions(less_strict: Configuration, more_strict: Configuration) -> bool:
    """
    Does less strict config produce superset of solutions to more strict config? Assuming the patient sets are the same
    :param less_strict: Configuration which we believe could be less strict
    :param more_strict: Configuration which we believe could be more strict
    :return:
    """
    # TODO: When we add more solvers and scorers this has to change
    _check_if_config_is_supported(less_strict)
    _check_if_config_is_supported(more_strict)

    breaking_parameters = ["enforce_same_blood_group",
                           "minimum_compatibility_index",
                           "require_new_donor_having_better_match_in_compatibility_index",
                           "require_new_donor_having_better_match_in_compatibility_index_or_blood_group"]

    # TODO: Implement
    raise NotImplementedError("TODO: Implement")
