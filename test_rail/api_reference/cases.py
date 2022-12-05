from typing import List

from test_rail.service.test_rail_session import Base


class CasesApi(Base):
    __sub_host = '/api/v2'

    def get_case(self, case_id: int) -> dict:
        """
        https://www.gurock.com/testrail/docs/api/reference/cases#getcase

        Returns an existing test case
        :param case_id: The ID of the test case
        :return: dict
        """
        return self._validate(self._request(
            'get', f'{self.__sub_host}/get_case/{case_id}'))

    def get_cases(self,
                  project_id: int = None,
                  suite_id: int = None) -> List[dict]:
        """
        https://www.gurock.com/testrail/docs/api/reference/cases#getcases

        Returns a list of test cases for a project or specific test suite
        (if the project has multiple suites enabled)
        :param project_id: The ID of the project -
            if project ID isn't indicated - take default project id
        :param suite_id: The ID of the test suite
            (optional if the project is operating in single suite mode)
        :return: list of cases
        """
        if project_id is None:
            project_id = self._session.default_project_id
        params = {}
        if suite_id is not None:
            params.update({'suite_id': suite_id})
        return self._validate_all(self._request(
            'get', f'{self.__sub_host}/get_cases/{project_id}', params=params))

    def get_history_for_case(self, case_id: int) -> List[dict]:
        """
    https://www.gurock.com/testrail/docs/api/reference/cases#gethistoryforcase

        Returns the edit history for a test case_id
        :param case_id: The ID of the test case
        :return:
        """
        return self._validate_all(self._request(
            'get', f'{self.__sub_host}/get_history_for_case/{case_id}'))

    def add_case(self,
                 section_id: int,
                 title: str,
                 template_id: int = None,
                 type_id: int = None,
                 priority_id: int = None,
                 estimate=None,
                 milestone_id: int = None,
                 refs: str = None, **kwargs) -> dict:
        """
        https://www.gurock.com/testrail/docs/api/reference/cases#addcase

        Creates a new test case
        :param section_id: The ID of the section the test case should be
                            added to
        :param title: The title of the test case (required)
        :param template_id: The ID of the template (field layout)
        :param type_id: The ID of the case type
        :param priority_id: The ID of the case priority
        :param estimate: The estimate, e.g. “30s” or “1m 45s”
        :param milestone_id: The ID of the milestone to link to the test case
        :param refs: A comma-separated list of references/requirements
        :return:
        """
        data = self._get_dict_from_locals(locals(), exclude=['section_id'])
        return self._validate(self._request(
            'post', f'{self.__sub_host}/add_case/{section_id}', data=data))

    def delete_case(self, case_id: int) -> int:
        """
        https://www.gurock.com/testrail/docs/api/reference/cases#deletecase

        Deletes an existing test case
        :param case_id: The ID of the test case
        :return: status code
        """
        return self._validate_status(self._request(
            'post', f'{self.__sub_host}/delete_case/{case_id}'))
