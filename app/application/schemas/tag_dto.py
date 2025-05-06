from pydantic import BaseModel

class TagDTO(BaseModel):
    id: int
    name: str

    model_config = {"from_attributes": True}
