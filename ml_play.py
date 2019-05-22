import arkanoid.communication as comm
import pickle
from arkanoid.communication import SceneInfo, GameInstruction
import numpy as np
import os.path

def ml_loop():
    filename = "forestTrained.sav" 
    filepath = os.path.join(os.path.dirname(__file__), filename)
    load_model = pickle.load(open(filepath, 'rb'))
    comm.ml_ready()

    while True:

        scene_info = comm.get_scene_info()

        if scene_info.status == SceneInfo.STATUS_GAME_OVER or \
            scene_info.status == SceneInfo.STATUS_GAME_PASS:
            scene_info = comm.get_scene_info()

        input_temp = np.array([scene_info.ball[0], scene_info.ball[1], scene_info.platform[0]])
        input = input_temp[np.newaxis, :]
        print(load_model.predict(input))
        print(input)
        if load_model.predict(input) > 0.1:
            comm.send_instruction(scene_info.frame, GameInstruction.CMD_RIGHT)
        elif load_model.predict(input) < -0.1:
            comm.send_instruction(scene_info.frame, GameInstruction.CMD_LEFT)
        else:
            comm.send_instruction(scene_info.frame, GameInstruction.CMD_NONE)