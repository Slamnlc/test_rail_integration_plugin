from typing import List

from test_rail.service.test_rail_session import Base


class StatusesApi(Base):
    __sub_host = '/api/v2'

    def get_statuses(self) -> List[dict]:
        """
        https://www.gurock.com/testrail/docs/api/reference/statuses

        Returns a list of available test statuses
        :return:
        """
        return self._validate_all(
            self._request('get', f'{self.__sub_host}/get_statuses'))

    def get_status_id_by_label(self, status_name: str) -> int:
        """
        Returns a status id by status name
        :param status_name: status name
        :return: status id
        """
        return next((status['id'] for status in self.get_statuses()
                     if status['label'].lower() == status_name), None)

    def get_statuses_ids_by_label(self, statuses_names: List[str]) -> List[int]:
        """
        Returns a statuses ids by statuses names
        :param statuses_names: statuses names
        :return: status id
        """
        statuses = self.get_statuses()
        return [next((st['id'] for st in statuses
                      if st['label'].lower() == status), None) for status in
                statuses_names]


class TestsApi(Base):
    __sub_host = '/api/v2'

    def get_test(self, test_id: int) -> dict:
        """
        https://www.gurock.com/testrail/docs/api/reference/tests#gettest

         Returns an existing test
        :param test_id:
        :return:
        """
        return self._validate(
            self._request('get', f'{self.__sub_host}/get_test/{test_id}'))

    def get_tests(self,
                  run_id: int,
                  status_id: str = None) -> List[dict]:
        """
        https://www.gurock.com/testrail/docs/api/reference/tests#gettests

        Returns a list of tests for a test run
        :param run_id: The ID of the test run
        :param status_id: A comma-separated list of status IDs to filter by
        :return:
        """
        params = {} if status_id is None else {'status_id': status_id}
        return self._validate_all(
            self._request('get', f'{self.__sub_host}/get_tests/{run_id}',
                          params=params))


class SectionsApi(Base):
    __sub_host = '/api/v2'

    def get_section(self, section_id: int) -> dict:
        """
        https://www.gurock.com/testrail/docs/api/reference/sections#getsection

        Returns an existing section
        :param section_id: The ID of the section
        :return:
        """
        return self._validate(self._request(
            'get', f'{self.__sub_host}/get_section/{section_id}'))

    def get_sections(self,
                     suite_id: int = None,
                     project_id: int = None) -> List[dict]:
        """
        https://www.gurock.com/testrail/docs/api/reference/sections#getsections

        Returns a list of sections for a project and test suite
        :param suite_id: The ID of the test suite (optional if the project is
                        operating in single suite mode)
        :param project_id: The ID of the project - if project ID isn't
                        indicated - take default project id
        :return:
        """
        params = {}
        if project_id is None:
            project_id = self._session.default_project_id
        if suite_id is not None:
            params = {'suite_id': suite_id}
        return self._validate_all(self._request(
            'get', f'{self.__sub_host}/get_sections/{project_id}',
            params=params))
