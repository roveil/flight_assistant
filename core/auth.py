from typing import Optional

from fastapi import Header, HTTPException, WebSocket, Query, status

from core.config import AUTH_TOKEN


async def get_token_header(x_token: str = Header('X-Token')) -> None:
    """
    Checks request for X-Token header validity
    :param x_token: request X-Token header value
    :raises HTTPException: 401 if X-Token header is invalid
    :return: None
    """
    if x_token != AUTH_TOKEN:
        raise HTTPException(status_code=401, detail="Unauthorized")


async def check_ws_token(websocket: WebSocket, token: Optional[str] = Query(None)) -> Optional[str]:
    """
    Checks websocket token query parameter for validity
    :param websocket: websocket connection
    :param token: query token parameter value
    :return: token if token is valid else None
    """
    check = (token == AUTH_TOKEN)

    if not check:
        await websocket.close(code=status.WS_1008_POLICY_VIOLATION)

    return token if check else None
