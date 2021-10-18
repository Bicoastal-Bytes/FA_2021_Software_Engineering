from yapf.yapflib.yapf_api import FormatFile
import os

def formatProject():
    with os.scandir("./wheel_of_jeopardy/") as dirs:
        for entry in dirs:
            print(entry.name)