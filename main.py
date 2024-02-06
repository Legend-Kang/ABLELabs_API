from fastapi import Body, FastAPI
from pydantic import BaseModel
from typing import Optional, Annotated


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
### Please note that the current API is provided as an example for discussing input and output formats.  
### The actual input and output values are subject to change based on mutual discussions and will be finalized at a later date.
### The overall structure of the API will be added at a later date, and proactive feedback is always welcome.
"""

app = FastAPI(
    title="ABLE Labs Notable API",
    description=description,
    version="0.0.1",
    contact={
        "name": "ABLE Labs Notable",
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
def set_hw_status(
    hw_status: Annotated[
        HW_Status,
        Body(
            openapi_examples={
                "led on": {
                    "summary": "led on example",
                    "value": {
                        "hw": "led",
                        "status": True,
                    },
                },
                "safety_lock off": {
                    "summary": "safety_lock off example",
                    "value": {
                        "hw": "safety_lock",
                        "status": False,
                    },
                },
            },
        ),
    ],
):
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
def set_preparation_info(
    preparation_info: Annotated[
        Preparation_Info,
        Body(
            examples=[
                {
                    "pipette": [
                        {"pipette_position": "left", "code": "8ch200p"},
                    ],
                    "deck": [
                        {
                            "deck_number": 1,
                            "code": "tiprack_ablelabs_200tip",
                            "available_tip": [
                                "111111111111",
                                "111111111111",
                                "111111111111",
                                "111111111111",
                                "111111111111",
                                "111111111111",
                                "111111111111",
                                "111111111111",
                            ],
                        },
                        {"deck_number": 2, "code": "spl_96wellplate"},
                    ],
                },
            ],
        ),
    ],
):
    return preparation_info


# @app.put("/preparation_info")
# def set_preparation_info(preparation_info: Preparation_Info):
#     return print(preparation_info)


"""### Step Event ###"""


@app.post("/step_info", tags=["Step"])
def set_step_info(
    step_info: Annotated[
        Step_Info,
        Body(
            examples=[
                {
                    "step_number": 1,
                    "step_name": "transfer",
                    "pipette_position": "left",
                    "volume": 100.0,
                    "transfer_method": "single",
                    "pipette_route": "serial",
                    "prevent_contam": False,
                    "reuse_tip": False,
                    "source": [
                        {
                            "deck_number": 5,
                            "well": [
                                "111111111111",
                                "111111111111",
                                "111111111111",
                                "111111111111",
                                "111111111111",
                                "111111111111",
                                "111111111111",
                                "111111111111",
                            ],
                            "pre_wet": False,
                            "tip_depth": 0,
                            "aspirate_speed": 0,
                            "pre_mix": {
                                "mix_volume": 0.0,
                                "mix_iteration": 0,
                                "mix_speed": 100,
                                "mix_delay": 0.0,
                            },
                            "pause_pipette": {
                                "height": 0.0,
                                "z_speed": 0,
                                "duration": 2.0,
                            },
                        }
                    ],
                    "target": [
                        {
                            "deck_number": 6,
                            "well": [
                                "111111111111",
                                "111111111111",
                                "111111111111",
                                "111111111111",
                                "111111111111",
                                "111111111111",
                                "111111111111",
                                "111111111111",
                            ],
                            "tip_depth": 0,
                            "post_mix": {
                                "mix_volume": 0.0,
                                "mix_iteration": 0,
                                "mix_speed": 100,
                                "mix_delay": 0.0,
                            },
                            "dispense_speed": 0,
                            "pause_pipette": {
                                "height": 0.0,
                                "z_speed": 0,
                                "duration": 2.0,
                            },
                            "blowout": "trash",
                        },
                    ],
                },
            ],
        ),
    ],
):
    return step_info


# @app.put("/preparation_info")
# def set_preparation_info(pipette: Pipette, deck: Deck):
#     return {pipette, deck}


@app.post("/step_available", tags=["Step"])
def get_step_available(
    step_number: Annotated[
        Step_Number,
        Body(
            examples=[
                {
                    "step_number": 1,
                },
            ],
        ),
    ],
):
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
def get_step_estimation_time(
    step_number: Annotated[
        Step_Number,
        Body(
            examples=[
                {
                    "step_number": 1,
                },
            ],
        ),
    ],
):
    return {"step_number": step_number.step_number, "estimated_time": "00:00:05"}


"""### Run Event ###"""


@app.post("/run_status", tags=["Run"])
def set_run_status(
    status: Annotated[
        Run_Status,
        Body(
            openapi_examples={
                "run": {
                    "summary": "run example",
                    "value": {
                        "status": "run",
                    },
                },
                "pause": {
                    "summary": "pause example",
                    "value": {
                        "status": "pause",
                    },
                },
                "stop": {
                    "summary": "stop example",
                    "value": {
                        "status": "stop",
                    },
                },
                "resume": {
                    "summary": "resume example",
                    "value": {
                        "status": "resume",
                    },
                },
            },
        ),
    ],
):
    return status
