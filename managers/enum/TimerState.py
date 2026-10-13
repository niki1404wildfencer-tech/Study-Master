from enum import Enum
class TimerState (Enum):
    STOPPED = "Stopped"
    PAUSED = "Paused"
    RUNNING = "running"
    FINISHED = "Finished"
    