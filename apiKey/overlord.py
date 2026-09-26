from langchain_core.tools import tool
from langgraph.runtime import get_runtime
from langchain.agents import create_agent
import numpy as np
import json, time, zmq, cv2
import datetime, os, imagezmq

@tool
def suggestion() -> str:
    """Suggests the best walking or driving methods for the user to improve mobility.

    Returns:
        str: The suggested methods of driving or walking.
    """
    


def rating(sec: float, dir: bool) -> None:
    """Drives the robot for a certain amount of seconds
    Parameters
        sec (float): How many second the robot will drive.
        dir (bool): True for foward False for backwards.
    
    Rules
        Do not move for more than 2 seconds
        Do not move for less than 0.2 seconds
    """
    sendCommand("drive "+str(sec)+" "+("foward" if dir else "back"))




@tool
def drive() -> bool:
    """
    Desc: Saves an image titled "view.jpg"

    Returns: 0 For no errors, 1 for error.
    """
    # print("hi")
    # while True:  # show streamed images until Ctrl-C
    sendCommand("picture")
    # takePic()
    # time.sleep(1)
    rpi_name, image = imageHub.recv_image()
    # imageHub.send_reply(0)
    # try:
    #     os.remove("view.jpg")
    # except Exception:
    #     print(Exception)
    print("recieved image")
    decimg = cv2.imdecode(image, 1)
    cv2.imwrite("view.jpg", decimg)
    # cv2.imshow(decimg, rpi_name)
    # cv2.imshow(rpi_name, image) # 1 window for each RPi
    cv2.waitKey(1)
    imageHub.send_reply(b'OK')
    return decimg