"""Contracts for https://jsonplaceholder.typicode.com. Unknown fields are rejected."""

from pydantic import BaseModel, ConfigDict, Field

EMAIL = r"^[^@\s]+@[^@\s]+\.[^@\s]+$"


class _Strict(BaseModel):
    model_config = ConfigDict(extra="forbid")


class GeoSchema(_Strict):
    lat: str
    lng: str


class AddressSchema(_Strict):
    street: str
    suite: str
    city: str
    zipcode: str
    geo: GeoSchema


class CompanySchema(_Strict):
    name: str
    catchPhrase: str
    bs: str


class UserSchema(_Strict):
    id: int
    name: str
    username: str
    email: str = Field(pattern=EMAIL)
    address: AddressSchema
    phone: str
    website: str
    company: CompanySchema


class PostSchema(_Strict):
    userId: int
    id: int
    title: str
    body: str


class CommentSchema(_Strict):
    postId: int
    id: int
    name: str
    email: str = Field(pattern=EMAIL)
    body: str
