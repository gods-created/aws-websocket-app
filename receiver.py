import asyncio, os, websockets, json
from websockets.sync.client import connect
from loguru import logger
from typing import Callable

from configs import WS_HOST

async def main() -> Callable[..., None]:
    if not WS_HOST:
        logger.warning('Invalid WS_HOST value!')
        return None
        
    websocket = connect(WS_HOST)
            
    try:
        while True:
            message = websocket.recv()
            logger.info(f'Received: {message}')
            
    except (websockets.exceptions.WebSocketException, Exception, ) as e:
        logger.error(str(e))
    
    finally:
        websocket.close()
        return None
    
if __name__ == '__main__':
    try:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        loop.run_until_complete(main())
        loop.close()
        
    except (Exception, KeyboardInterrupt, ) as e:
        logger.error(str(e))

