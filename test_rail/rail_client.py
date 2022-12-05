import json
from datetime import datetime
from os import environ

from test_rail.api_reference.cases import CasesApi
from test_rail.api_reference.milestones import MilestonesApi
from test_rail.api_reference.results import ResultsApi
from test_rail.api_reference.runs import RunsApi
from test_rail.api_reference.small_api import StatusesApi, TestsApi, SectionsApi
from test_rail.service.test_rail_session import Session


class TestRail(Session):
    def __init__(self, host: str, username: str, token: str,
                 default_project_id: int = None):
        super().__init__(host, username, token, default_project_id)
        statuses = self.statuses.get_statuses_ids_by_label(
            ['passed', 'retest', 'skipped', 'blocked'])
        self.pass_status, self.fail_status, self.skip_status, self. \
            blocked_status = statuses
        if self.skip_status is None:
            self.skip_status = self.blocked_status

    @property
    def cases(self):
        return CasesApi(self)

    @property
    def runs(self):
        return RunsApi(self)

    @property
    def results(self):
        return ResultsApi(self)

    @property
    def milestones(self):
        return MilestonesApi(self)

    @property
    def statuses(self):
        return StatusesApi(self)

    @property
    def api_tests(self):
        return TestsApi(self)

    @property
    def sections(self):
        return SectionsApi(self)

    def make_backup(self, cases_file: str = None, sections_file: str = None):
        date = datetime.now().strftime("%Y-%m-%d %H:%m")
        if cases_file is None:
            cases_file = f'cases_backup_{date}.json'
        if sections_file is None:
            sections_file = f'sections_backup_{date}.json'

        assert cases_file.split('.')[-1] == 'json', \
            "Wrong file format for cases backup file. Must be JSON"

        assert sections_file.split('.')[-1] == 'json', \
            "Wrong file format for sections backup file. Must be JSON"

        cases = self.cases.get_cases()
        sections = self.sections.get_sections()

        with open(cases_file, 'w') as file:
            file.write(json.dumps(cases))

        with open(sections_file, 'w') as file:
            file.write(json.dumps(sections))


if __name__ == '__main__':
    tr = TestRail(host=environ.get('TEST_RAIL_HOST'),
                  token=environ.get('TEST_RAIL_TOKEN'),
                  username=environ.get('TEST_RAIL_USERNAME'),
                  default_project_id=1)
    tr.make_backup()
