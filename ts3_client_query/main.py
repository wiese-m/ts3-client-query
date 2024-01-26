import asyncio
import os
from pprint import pprint

from ts3_client_query.client import TS3Client
from ts3_client_query.definitions.target import TargetMode


async def main() -> None:
    client = TS3Client()
    await client.connect()
    await client.auth(os.environ['APIKEY'])
    me = await client.whoami()
    print(me)
    await client.send_text_message('This is a test message!', TargetMode.CLIENT, client_id=me.client_id)
    users = await client.get_users()
    pprint(users)
    client.close()

if __name__ == '__main__':
    asyncio.run(main())
