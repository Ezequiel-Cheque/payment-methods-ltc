from pydantic import BaseModel, Field
from typing import List


class paymentMethodSchema(BaseModel):
    name: str = Field(description="")
    code: str = Field(description="")
    url_image: str = Field(description="")
    form: str = Field(description="")
    id_country: str = Field(description="")
    id_pay_type: str = Field(description="")
    

class createManySchema(BaseModel):
    id_psp: str = Field(description="")
    endpoint: str = Field(description="")
    paymentMethods: List[paymentMethodSchema] = Field(description="")
    

class formatSchema(BaseModel):
    form: str = Field(description="")
    id_country: str = Field(description="")
    id_pay_type: str = Field(description="")
    data: List[dict] = Field(description="")
