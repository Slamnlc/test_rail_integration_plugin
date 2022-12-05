import base64
from json import dumps
from typing import List

import requests
from requests import Response

from test_rail.service.test_rail_errors import TestRailError


class Session:
    def __init__(self, host: str, username: str, token: str,
                 default_project_id: int = None):
        """
        Insert your api server
        :param host:
        :param username: your username
        :param token: tour API token
        :param default_project_id: default id of testrail project
        """
        self.__host = host
        self._results = []
        self._session = requests.Session()
        self._session.auth = Auth(username, token)
        self._session.headers['Content-Type'] = 'application/json'
        self.default_project_id = default_project_id
        self.__host = f'{self.__host}/index.php?'
        self.result_url = f'{self.__host}/tests/view'
        self.case_url = f'{self.__host}/cases/view/'

    def _request(self, method: str, url: str, data: dict = None,
                 params: dict = None) -> Response:
        methods = ('get', 'post', 'delete')
        if method.lower() in methods:
            data = dumps(data) if data is not None else ''

            return self._session.request(
                method=method,
                url=f'{self.__host}{url}',
                data=data,
                params=params)
        else:
            raise TestRailError(f'{method} is not allowed method. '
                                f'Allowed methods: {",".join(methods)}')

    def _get_all(self):
        pass


class Base:
    def __init__(self, session: Session):
        self._session: Session = session

    def _request(self, method: str, url: str, data: dict = None,
                 params: dict = None) -> Response:
        return self._session._request(method, url, data, params)

    @staticmethod
    def _validate(response: Response) -> dict:
        assert response.status_code < 400, \
            f"Error until request {response.text}"
        return response.json()

    def _validate_all(self, response: Response) -> List[dict]:
        assert response.status_code < 400, \
            f"Error until request {response.text}"
        data = response.json()
        if isinstance(data, list):
            return data
        else:
            main_key = next(key for key in data.keys() if
                            key not in ['offset', 'limit', 'size', '_links'])
            return_data = data[main_key]
            request = response.request
            while data['size'] == 250:
                sub_response = self._session._request(request.method,
                                                      url=data['_links'][
                                                          'next'])
                assert sub_response.status_code < 400, \
                    f"Error until request {sub_response.text}"
                data = sub_response.json()
                return_data.extend(data[main_key])

            return return_data

    @staticmethod
    def _validate_status(response: Response) -> int:
        assert response.status_code < 400, \
            f"Error until request {response.text}"
        return response.status_code

    @staticmethod
    def _get_dict_from_locals(locals_dict: dict,
                              replace_underscore: bool = False,
                              exclude: list = None) -> dict:
        exclude = ('self', 'kwargs') if exclude is None else tuple(
            ['self', 'kwargs'] + exclude)
        result = {key if replace_underscore else key: value for key, value in
                  locals_dict.items()
                  if key not in exclude and '__py' not in key
                  and value is not None}
        if 'kwargs' in locals_dict:
            result.update(locals_dict['kwargs'])
        return result


class Auth:
    def __init__(self, username, password):
        self.data = base64.b64encode(
            b':'.join((username.encode('ascii'),
                       password.encode('ascii')))).strip().decode('ascii')

    def __call__(self, r):
        r.headers['Authorization'] = f'Basic {self.data}'
        return r
