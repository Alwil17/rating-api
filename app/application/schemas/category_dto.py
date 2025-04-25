from pydantic import BaseModel

class CategoryDTO(BaseModel):
    id: int
    name: str

    model_config = {"from_attributes": True}