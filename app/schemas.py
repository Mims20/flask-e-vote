# from flask import Form
from typing import Optional

from pydantic import BaseModel, EmailStr


# get form data in dict
# def form_body(cls):
#     cls.__signature__ = cls.__signature__.replace(
#         parameters=[
#             arg.replace(default=Form(...))
#             for arg in cls.__signature__.parameters.values()
#         ]
#     )
#     return cls


# @form_body
class Register(BaseModel):
    email: EmailStr
    password: str


# @form_body
class Candidate(BaseModel):
    first_name: str
    last_name: str
    position: str


class TokenData(BaseModel):
    id: Optional[str] = None
