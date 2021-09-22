import uvicorn
from fastapi import Depends, FastAPI
from fastapi_utils.tasks import repeat_every

from core.auth import get_token_header
from core.db import engine
from core.config import DEBUG_PORT
from flights.views import user_router
from locations.views import country_router, city_router
from meetups.tasks import clean_meetup_redis_queues
from meetups.views import boarding_pass_router
from meetups.ws import meetup_ws_router

description = """
Flight assistant API

## CRUD functionality realised for models
* **User**
* **City**
* **Country**

Additional websocket paths:
* /ws/meetup/{meetup_id}/map - every 10 seconds returns statistics about last arrived user. 
**token:** required query parameter (default=X-Token)

* /ws/meetup/{meetup_id}/boarding - show last arrived user’s statistics in realtime when check validity API is called.  
**token:** required query parameter (default=X-Token)
"""

app = FastAPI(title="Flight Assistant API",
              description=description,
              version="0.0.1",
              contact={
                  "name": "roveil",
                  "url": "https://github.com/roveil",
                  "email": "dvsroveil@gmail.com",
              },
              license_info={
                  "name": "Apache 2.0",
                  "url": "https://www.apache.org/licenses/LICENSE-2.0.html",
              },
              )

app.include_router(country_router, dependencies=[Depends(get_token_header)])
app.include_router(city_router, dependencies=[Depends(get_token_header)])
app.include_router(boarding_pass_router, dependencies=[Depends(get_token_header)])
app.include_router(user_router, dependencies=[Depends(get_token_header)])
app.include_router(meetup_ws_router)


@app.on_event("shutdown")
async def shutdown():
    await engine.dispose()


@app.on_event("startup")
@repeat_every(seconds=60 * 10)
async def remove_expired_tokens_task() -> None:
    await clean_meetup_redis_queues()


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=DEBUG_PORT)
