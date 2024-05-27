from fastapi import FastAPI
from fastapi.responses import JSONResponse
import uvicorn
import toml
import os

from fl.preprocessing import load_mnist
from api.challenges import (
    challenge_backdoor,
    challenge_easy_poison,
    challenge_intro_poison,
    challenge_force_prediction
)

DIR_PATH = os.path.dirname(os.path.realpath(__file__))
config = toml.load(DIR_PATH + "/config.toml")
app = FastAPI()
dataset = load_mnist()
x_train, y_train, x_test, y_test = dataset

challenges = {
    "1": challenge_intro_poison,
    "2": challenge_easy_poison,
    "3": challenge_backdoor,
    "4": challenge_force_prediction
}


@app.get("/healthcheck")
async def healthcheck():
    return JSONResponse(content={"message": "Statut : en pleine forme !"}, status_code=200)


@app.post("/challenges/{challenge_id}")
async def challenge_poison(challenge_id: int, data: dict):
    if str(challenge_id) not in challenges.keys():
        message = "Ce challenge n'existe pas encore O.o"
    else:
        message = challenges[str(challenge_id)](data, x_test, y_test)

    return JSONResponse(status_code=200, content={
        "message": message
    })


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
