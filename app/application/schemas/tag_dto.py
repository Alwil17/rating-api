from pydantic import BaseModel, Field

class TagBaseDTO(BaseModel):
    name: str = Field(..., example="Technology")

class TagDTO(TagBaseDTO):
    id: int = Field(..., example=1)

    class Config:
        orm_mode = True

class TagCreateDTO(TagBaseDTO):
    pass

class TagUpdateDTO(TagBaseDTO):
    pass
