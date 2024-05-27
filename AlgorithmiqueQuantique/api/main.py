from fastapi import FastAPI
from fastapi.responses import JSONResponse
from typing import Dict, List, Tuple, Union
import uvicorn
import toml
import os

from api.challenges import challenge_intro, challenge_bb84, challenge_multiple_systems, challenge_reverse

DIR_PATH = os.path.dirname(os.path.realpath(__file__))
config = toml.load(DIR_PATH + "/config.toml")
app = FastAPI()
challenges = {
    "1": challenge_intro,
    "2": challenge_bb84,
    "3": challenge_multiple_systems,
    "4": challenge_reverse
}


@app.get("/healthcheck")
async def healthcheck() -> JSONResponse:
    return JSONResponse(content={"message": "Statut : en pleine forme !"})


@app.post("/challenges/{challenge_id}")
async def challenge(
        challenge_id: int,
        data: Dict[str, Union[
            List[List[Tuple[float, float]]],
            List[Tuple[float, float]]
        ]]
) -> JSONResponse:
    if challenges[str(challenge_id)](data):
        message = f"GG ! Voici le drapeau : {config['flags'][str(challenge_id)]}"
    else:
        message = "Raté !"
    return JSONResponse(content={
        "message": message
    })


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
