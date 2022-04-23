from typing import TypedDict


class CodeMessage(TypedDict):
    code: int
    msg: str


class ErrCode:
    NOT_INIT = CodeMessage(
        code=100001, msg='Not initialized. Please set one admin user.')
    PWD_ERR = CodeMessage(
        code=200001, msg='Username or password wrong. Please login again.')
