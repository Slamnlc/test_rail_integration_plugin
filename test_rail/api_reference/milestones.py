from typing import List

from test_rail.service.test_rail_session import Base


class MilestonesApi(Base):
    __sub_host = '/api/v2'

    def get_milestone(self, milestone_id: int) -> dict:
        """
    https://www.gurock.com/testrail/docs/api/reference/milestones#getmilestone

        Returns an existing milestone
        :param milestone_id: The ID of the milestone
        :return: Milestone object
        """
        return self._validate(self._request(
            'get', f'{self.__sub_host}/get_milestone/{milestone_id}'))

    def get_milestones(self, project_id: int = None) -> List[dict]:
        """
    https://www.gurock.com/testrail/docs/api/reference/milestones#getmilestones

        Returns the list of milestones for a project
        :param project_id: The ID of the project -
            if project ID isn't indicated - take default project id
        :return: list of milestones
        """
        if project_id is None:
            project_id = self._session.default_project_id
        return self._validate_all(self._request(
            'get', f'{self.__sub_host}/get_milestones/{project_id}'))
