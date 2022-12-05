from typing import List

from test_rail.service.test_rail_session import Base


class RunsApi(Base):
    __sub_host = '/api/v2'

    def get_run(self, run_id: int) -> dict:
        """
        https://www.gurock.com/testrail/docs/api/reference/runs#getrun

        Returns an existing test run
        :param run_id: The ID of the test run
        :return:
        """
        return self._validate(self._request(
            'get', f'{self.__sub_host}/get_run/{run_id}'))

    def get_runs(self, project_id: int = None) -> List[dict]:
        """
        https://www.gurock.com/testrail/docs/api/reference/runs#getruns

        Returns a list of test runs for a project
        :param project_id: The ID of the project -
            if project ID isn't indicated - take default project id
        :return: list or runs
        """
        if project_id is None:
            project_id = self._session.default_project_id
        return self._validate_all(self._request(
            'get', f'{self.__sub_host}/get_runs/{project_id}'))

    def add_run(self,
                suite_id: int = None,
                name: str = None,
                description: str = None,
                milestone_id: int = None,
                assignedto_id: int = None,
                include_all: bool = None,
                case_ids: (str, list) = None,
                refs: str = None,
                project_id: int = None) -> dict:
        """
        https://www.gurock.com/testrail/docs/api/reference/runs#addrun

        Creates a new test run
        :param suite_id: The ID of the test suite for the test run
                (optional if the project is operating in single suite mode,
                required otherwise)
        :param name: The name of the test run
        :param description: The description of the test run
        :param milestone_id: The ID of the milestone to link to the test run
        :param assignedto_id: The ID of the user the test run should be
                                assigned to
        :param include_all: True for including all test cases of the test
                    suite and false for a custom case selection (default: true)
        :param case_ids: An array of case IDs for the custom case selection
        :param refs: A comma-separated list of references/requirements
                        (Requires TestRail 6.1 or later)
        :param project_id: The ID of the project -
                        if project ID isn't indicated - take default project id
        :return:
        """
        if project_id is None:
            project_id = self._session.default_project_id
        data = self._get_dict_from_locals(locals(), exclude=['project_id'])
        return self._validate(self._request(
            'post', f'{self.__sub_host}/add_run/{project_id}'))

    def update_run(self,
                   run_id: int,
                   name: str = None,
                   description: str = None,
                   milestone_id: int = None,
                   include_all: bool = None,
                   case_ids: str = None,
                   refs: str = None) -> dict:
        """
        https://www.gurock.com/testrail/docs/api/reference/runs#updaterun

        Updates an existing test run
        (partial updates are supported, i.e. you can submit and
        update specific fields only).
        :param run_id: The ID of the test run
        :param name: The name of the test run
        :param description: The description of the test run
        :param milestone_id: The ID of the milestone to link to the test run
        :param include_all: True for including all test cases of the test suite
                and false for a custom case selection
        :param case_ids: An array of case IDs for the custom case selection
        :param refs: A comma-separated list of references/requirements
        :return:
        """
        data = self._get_dict_from_locals(locals())
        return self._validate(
            self._request('post', f'{self.__sub_host}/update_run/{run_id}',
                          data=data))

    def is_have_run(self, run_id: int) -> bool:
        """
        Check if run exists
        :param run_id: The ID of the test run
        :return: boolean value
        """
        return 'error' not in self._request(
            'get', f'{self.__sub_host}/get_run/{run_id}').json()
