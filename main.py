from fastapi import FastAPI
from pydantic import BaseModel
from typing import Optional


class Pipette(BaseModel):
    pipette_position: str
    code: str


class Deck(BaseModel):
    deck_number: int
    code: str
    available_tip: Optional[list[str]] = None


class Mix(BaseModel):
    mix_volume: float
    mix_iteration: int
    mix_speed: int
    mix_delay: float


class Pause_Pipette(BaseModel):
    height: float
    z_speed: int
    duration: float


class Source(BaseModel):
    deck_number: int
    well: list[str]
    pre_wet: bool
    tip_depth: int
    aspirate_speed: int
    pre_mix: Mix
    pause_pipette: Pause_Pipette


class Target(BaseModel):
    deck_number: int
    well: list[str]
    tip_depth: int
    post_mix: Mix
    pause_pipette: Pause_Pipette
    blowout: str


class Step_Number(BaseModel):
    step_number: int


class HW_Status(BaseModel):
    hw: str
    status: bool


class Preparation_Info(BaseModel):
    pipette: list[Pipette]
    deck: list[Deck]


class Step_Info(BaseModel):
    step_number: int
    step_name: str
    pipette_position: str
    volume: float
    transfer_method: str
    pipette_route: str
    prevent_contam: bool
    reuse_tip: bool
    source: Source
    target: Target


class Run_Status(BaseModel):
    status: str


tags_metadata = [
    {
        "name": "HW Control",
        "description": "Controls sensors and LEDs inside Notable.",
    },
    {
        "name": "Preparation",
        "description": "It shows the information of the experiment preparation stage.",
    },
    {
        "name": "Step",
        "description": "Get details about your experiment.",
    },
    {
        "name": "Run",
        "description": "Control over equipment status.",
    },
]

description = """
## ABLE Labs API helps you do awesome stuff. 🚀
"""

app = FastAPI(
    title="ABLE Labs API",
    description=description,
    version="0.0.1",
    contact={
        "name": "ABLE Labs",
        "url": "https://ablelabsinc.com/en/home/",
        "email": "sophie@ablelabsinc.com",
    },
    openapi_tags=tags_metadata,
)


# @app.get("/")
# async def root():
#     return {"message": "ABLELabs`s API"}


"""### HW Control Event ###"""


@app.post("/hw_status", tags=["HW Control"])
def set_hw_status(hw_status: HW_Status):
    return f"{hw_status} Set Complete"


# @app.put("/hw_status")
# def set_hw_status(hw_status: HW_Status):
#     print(hw_status)


"""### Preparation Event ###"""


@app.get("/pipette_info", tags=["Preparation"])
def get_pipette_info():
    return {
        "pipettes": [
            {"code": "8ch200p", "channel": 8, "volume": 200},
            {"code": "1ch1000p", "channel": 1, "volume": 1000},
        ]
    }


@app.get("/labware_info", tags=["Preparation"])
def get_labware_info():
    return {
        "labwares": [
            {
                "type": "tiprack",
                "code": "tiprack_ablelabs_200tip",
                "volume": 200,
                "rows": 8,
            },
        ]
    }


@app.post("/preparation_info", tags=["Preparation"])
def set_preparation_info(preparation_info: Preparation_Info):
    return preparation_info


# @app.put("/preparation_info")
# def set_preparation_info(preparation_info: Preparation_Info):
#     return print(preparation_info)


"""### Step Event ###"""


@app.post("/step_info", tags=["Step"])
def set_step_info(step_info: Step_Info):
    return step_info


# @app.put("/preparation_info")
# def set_preparation_info(pipette: Pipette, deck: Deck):
#     return {pipette, deck}


@app.post("/step_available", tags=["Step"])
def get_step_available(step_number: Step_Number):
    if step_number.step_number == 1:
        return {
            "step_number": step_number.step_number,
            "is_avaliable": True,
            "tip_info": {
                "deck_number": 7,
                "well": [
                    "111111000000",
                    "111111000000",
                    "111111000000",
                    "111111000000",
                    "111111000000",
                    "111111000000",
                    "111111000000",
                    "111111000000",
                ],
            },
        }

    else:
        return {
            "step_number": step_number.step_number,
            "is_avaliable": False,
            "lacking_tip": 30,
        }


@app.post("/step_estimation_time", tags=["Step"])
def get_step_estimation_time(step_number: Step_Number):
    return {"step_number": step_number.step_number, "estimated_time": "00:00:05"}


"""### Run Event ###"""


@app.post("/run_status", tags=["Run"])
def set_run_status(status: Run_Status):
    return status
