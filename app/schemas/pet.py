from pydantic import BaseModel


class PetBase(BaseModel):
    type: str
    breed: str | None = None
    weight: float | None = None
    resident_id: int


class PetCreate(PetBase):
    pass


class PetRead(PetBase):
    id: int

    class Config:
        orm_mode = True
