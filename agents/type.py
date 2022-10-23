from enum import Enum


class ModelType(Enum):
    QTABLE = 1
    DEEP_QTABLE = 2


class TargetType(Enum):
    REWARD = 1
    QTABLE = 2
