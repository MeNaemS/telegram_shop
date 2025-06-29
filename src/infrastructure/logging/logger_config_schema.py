from typing import List, TypedDict, Any


class LoggerFormattersDefault(TypedDict):
    format: str


class LoggerFormattersColored(TypedDict):
    __call__: str
    format: str


class LoggerFormattersSchema(TypedDict):
    default: LoggerFormattersDefault
    colored: LoggerFormattersColored


class LoggerHandlerConsole(TypedDict):
    class_: str
    formatter: str
    level: str
    stream: Any


class LoggerHandlerFile(TypedDict):
    class_: str
    filename: str
    maxBytes: int
    backupCount: int
    formatter: str
    level: str


class LoggerHandlersSchema(TypedDict):
    console: LoggerHandlerConsole
    file: LoggerHandlerFile


class LoggerRootSchema(TypedDict):
    handlers: List[str]
    level: str


class LoggerConfig(TypedDict):
    level: str
    handlers: List[str]
    propagate: bool


class LoggersSchema(TypedDict):
    src: LoggerConfig
    config: LoggerConfig
    uvicorn: LoggerConfig
    uvicorn_access: LoggerConfig


class LoggerConfigSchema(TypedDict):
    version: int
    disable_existing_loggers: bool
    formatters: LoggerFormattersSchema
    handlers: LoggerHandlersSchema
    root: LoggerRootSchema
    loggers: LoggersSchema