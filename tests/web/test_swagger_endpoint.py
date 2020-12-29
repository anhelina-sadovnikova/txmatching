from swagger_unittest import swagger_test

from tests.test_utilities.generate_swagger import PATH_TO_SWAGGER_YAML
from tests.test_utilities.populate_db import ADMIN_WITH_DEFAULT_TXM_EVENT
from tests.test_utilities.prepare_app import DbTests
from txmatching.utils.get_absolute_path import get_absolute_path
from txmatching.web import (API_VERSION, SERVICE_NAMESPACE,
                            TXM_EVENT_NAMESPACE, USER_NAMESPACE)


class TestSwaggerEndpoints(DbTests):

    def test_server_not_logged_in(self):
        special_status_codes_for_paths = {
            'get': {
                f'{API_VERSION[1:]}/{SERVICE_NAMESPACE}/status': [200],
                f'{API_VERSION[1:]}/{SERVICE_NAMESPACE}/version': [200],
            }
        }
        with self.app.test_client() as client:
            swagger_test(swagger_yaml_path=PATH_TO_SWAGGER_YAML, app_client=client, expected_status_codes={401},
                         special_status_code_for_paths=special_status_codes_for_paths)

    def test_server_logged_in(self):
        self.txm_event_db_id = self.fill_db_with_patients(
            get_absolute_path('/tests/resources/patient_data_2020_07_obfuscated.xlsx')
        )
        special_status_code_for_paths = {
            'post': {
                f'{API_VERSION[1:]}/{USER_NAMESPACE}/login': [401],
                f'{API_VERSION[1:]}/{USER_NAMESPACE}/otp': [403],
            },
            'put': {
                f'{API_VERSION[1:]}/{USER_NAMESPACE}/otp': [403],
                f'{API_VERSION[1:]}/{USER_NAMESPACE}/change-password': [401],
                f'{API_VERSION[1:]}/{TXM_EVENT_NAMESPACE}/patients': [403],
            }
        }
        # we need this user as we need the report to be generated from filled txm event, but we create an empty
        # txm event in the process of running the swagger
        self.login_with_credentials(ADMIN_WITH_DEFAULT_TXM_EVENT)
        with self.app.test_client() as client:
            swagger_test(swagger_yaml_path=PATH_TO_SWAGGER_YAML,
                         app_client=client,
                         expected_status_codes={200, 201},
                         extra_headers=self.auth_headers,
                         special_status_code_for_paths=special_status_code_for_paths
                         )