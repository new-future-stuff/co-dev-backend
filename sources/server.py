from fastapi import FastAPI

import api.users


app = FastAPI()

app.include_router(api.users.router)
