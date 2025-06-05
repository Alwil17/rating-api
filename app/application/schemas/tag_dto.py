from pydantic import BaseModel, ConfigDict, Field

class TagBaseDTO(BaseModel):
    name: str = Field(..., example="Technology")

class TagDTO(TagBaseDTO):
    id: int = Field(..., example=1)

    model_config = ConfigDict(from_attributes=True, extra='allow')

class TagCreateDTO(TagBaseDTO):
    pass

class TagUpdateDTO(TagBaseDTO):
    pass
