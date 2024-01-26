import re

import telnetlib3
from telnetlib3 import TelnetReader, TelnetWriter

from ts3_client_query.definitions.target import TargetMode
from ts3_client_query.definitions.user import User, Myself


class TS3Client:
    def __init__(self, host: str = 'localhost', port: int = 25639) -> None:
        self.host = host
        self.port = port
        self.reader: TelnetReader | None = None
        self.writer: TelnetWriter | None = None
        self.authorized: bool = False

    async def connect(self) -> None:
        self.reader, self.writer = await telnetlib3.open_connection(self.host, self.port)
        content: str = await self.reader.read(1024)
        print(content)

    def close(self) -> None:
        self.writer.close()

    async def auth(self, apikey: str) -> None:
        self._write(f'auth apikey={apikey}')
        response = await self._read_line()
        error = self._parse_response(response)
        if error.get('id') != '0':
            raise ValueError(f'Authorization failed [reason: {error.get("msg")}]')
        else:
            self.authorized = True

    async def whoami(self) -> Myself:
        self._check_auth()
        self._write('whoami')
        response = await self._read_line()
        await self._read_line()
        myself = self._parse_response(response)
        return Myself(
            client_id=int(myself['clid']),
            channel_id=int(myself['cid']),
        )

    # todo: implement sending messages with multiple lines (recursive?)
    async def send_text_message(self, message: str, target_mode: TargetMode, *, client_id: int | None = None) -> None:
        self._check_auth()
        target = '' if client_id is None else f'target={client_id}'
        message = message.replace(' ', r'\s')
        self._write(f'sendtextmessage targetmode={target_mode.value} {target} msg={message}')
        response = await self._read_line()
        error = self._parse_response(response)
        if error.get('id') != '0':
            raise ValueError(f'Failed to send text message [reason: {error.get("msg")}]')

    # todo: implement all optional modifier parameters
    async def get_users(self) -> list[User]:
        self._check_auth()
        self._write('clientlist')
        users_response = await self._read_line()
        error_response = await self._read_line()
        error = self._parse_response(error_response)
        if error.get('id') != '0':
            raise ValueError(f'Failed to list all users [reason: {error.get("msg")}]')
        users = self._parse_response_with_sep(users_response)
        print(users)
        return [
            User(
                client_id=int(user['clid']),
                channel_id=int(user['cid']),
                client_database_id=int(user['client_database_id']),
                client_nickname=user['client_nickname'],
                client_type=int(user['client_type']),
            )
            for user in users
        ]

    # parser
    @staticmethod
    def _parse_response(response: str) -> dict[str, str]:
        response = response.replace(r'\s', ' ')
        pattern = re.compile(r'(\w+)=(.+?)\s*(?=\w+=|$)')
        return dict(pattern.findall(response))

    # parser
    @staticmethod
    def _parse_response_with_sep(response: str, sep: str = '|') -> list[dict[str, str]]:
        response = response.replace(r'\s', ' ')
        info_list = response.split(sep)
        pattern = re.compile(r'(\w+)=(.+?)\s*(?=\w+=|$)')
        return [dict(pattern.findall(info)) for info in info_list]

    # validator
    def _check_auth(self) -> None:
        if not self.authorized:
            raise ValueError(f'Authorization needed')

    def _write(self, data: str) -> None:
        self.writer.write(data)
        self.writer.write('\n')

    async def _read_line(self, print_line: bool = True) -> str:
        line: str = await self.reader.readline()
        await self.reader.readline()  # b'\r'
        if print_line:
            print(line)
        return line
