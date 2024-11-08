import asyncio, os, websockets, json
from websockets.sync.client import connect
from loguru import logger
from os import getenv
from typing import Callable

from configs import WS_HOST

async def main() -> Callable[..., None]:
    if not WS_HOST:
        logger.warning('Invalid WS_HOST value!')
        await main()
        
    message = str(input('Your message: '))
        
    try:
        data = {
            'action': 'send_message',
            'message': message
        }
        
        with connect(WS_HOST) as websocket:
            websocket.send(json.dumps(data))
            response = websocket.recv()
            logger.info(f'Received: {response}')
            
    except (websockets.exceptions.WebSocketException, Exception, ) as e:
        logger.error(str(e))
    
    finally:
        await main()
    
if __name__ == '__main__':
    try:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        loop.run_until_complete(main())
        loop.close()
        
    except (Exception, KeyboardInterrupt, ) as e:
        logger.error(str(e))
