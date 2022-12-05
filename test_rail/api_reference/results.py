from datetime import datetime
from itertools import chain
from typing import List

from test_rail.service.helpers import split_list
from test_rail.service.test_rail_session import Base


class ResultsApi(Base):
    __sub_host = '/api/v2'

    def get_results(self, test_id: int) -> List[dict]:
        """
        https://www.gurock.com/testrail/docs/api/reference/results#getresults

        Returns a list of test results for a test
        :param test_id: The ID of the test
        :return:
        """
        return self._validate_all(self._request(
            'get', f'{self.__sub_host}/get_results/{test_id}'))

    def get_results_for_case(self,
                             run_id: int,
                             case_id: int,
                             defects_filter: str = None,
                             status_id: str = None) -> List[dict]:
        """
    https://www.gurock.com/testrail/docs/api/reference/results#getresultsforcase

        Returns a list of test results for a test run and case combination
        :param run_id: The ID of the test run
        :param case_id: The ID of the test case
        :param defects_filter: A single Defect ID (e.g. TR-1, 4291, etc.)
        :param status_id: A comma-separated list of status IDs to filter by
        :return:
        """
        params = self._get_dict_from_locals(
            locals(), exclude=['run_id', 'case_id'])
        return self._validate_all(self._request(
            'get', f'{self.__sub_host}/get_results_for_case/{run_id}/{case_id}',
            params=params))

    def get_results_for_run(self, run_id: int,
                            created_after: datetime = None,
                            created_before: datetime = None,
                            created_by: str = None,
                            defects_filter: str = None,
                            status_id: str = None) -> List[dict]:
        """
    https://www.gurock.com/testrail/docs/api/reference/results#getresultsforrun

        Returns a list of test results for a test run
        :param run_id: The ID of the test run
        :param created_after: Only return test results created after this date
        :param created_before: Only return test results created before this date
        :param created_by: A comma-separated list of creators (user IDs)
                        to filter by
        :param defects_filter: A single Defect ID (e.g. TR-1, 4291, etc.)
        :param status_id: A comma-separated list of status IDs to filter by
        :return:
        """
        if created_after is not None:
            created_after = int(created_after.timestamp())
        if created_before is not None:
            created_before = int(created_before.timestamp())
        params = self._get_dict_from_locals(locals(), exclude=['run_id'])
        return self._validate_all(self._request(
            'get', f'{self.__sub_host}/get_results_for_run/{run_id}',
            params=params))

    def add_results(self,
                    run_id: int,
                    results: (list, tuple)) -> List[dict]:
        """
        https://www.gurock.com/testrail/docs/api/reference/results#addresults

        Adds one or more new test results, comments or assigns one or more
        tests
        :param run_id: The ID of the test run the results should be added to.
        :param results:
        :return: list of results
        """
        url = 'add_results'
        if len(results) > 1000:
            result = []
            for sub_result in split_list(results, separator=1000):
                data = {'results': sub_result}
                result.append(
                    self._validate(self._request(
                        'post', f'{self.__sub_host}/{url}/{run_id}',
                        data=data)))
            return tuple(chain.from_iterable(result))

        else:
            data = {'results': results}
            return self._validate_all(self._request(
                'post', f'{self.__sub_host}/{url}/{run_id}', data=data))
