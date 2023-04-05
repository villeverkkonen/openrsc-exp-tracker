from fastapi import FastAPI
from players import players
from fastapi.staticfiles import StaticFiles
from hiscores import hiscores, dummy_hiscores


app = FastAPI(
    title="OpenRSC Skilling Competition",
    description="Tracks players experience development"
)
api_app = FastAPI(title="API")
app.mount("/api", api_app)
app.mount("/", StaticFiles(directory="../client/dist", html=True), name="client")



@api_app.get('/hiscores')
async def get_hiscores():
    # return hiscores
    return dummy_hiscores