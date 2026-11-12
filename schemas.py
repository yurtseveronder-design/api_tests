from pydantic import BaseModel

class GeoSchema(BaseModel):
    lat: str
    lng: str

class AddressSchema(BaseModel):
    street: str
    suite: str
    city: str
    zipcode: str
    geo: GeoSchema

class CompanySchema(BaseModel):
    name: str
    catchPhrase: str
    bs: str

class UserResponseSchema(BaseModel):
    id: int
    name: str
    username: str
    email: str
    address: AddressSchema
    phone: str
    website: str
    company: CompanySchema

class PostResponseSchema(BaseModel):
    userId: int
    id: int
    title: str
    body: str