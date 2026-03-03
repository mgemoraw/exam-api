from pydantic import BaseModel, EmailStr, ConfigDict
from datetime import datetime
from decimal import Decimal
from pydantic.alias_generators import to_camel


class AppBaseModel(BaseModel):
    model_config = ConfigDict(
        alias_generator=to_camel,
        populate_by_name=True,
        json_encoders={
            datetime: lambda v: v.isoformat(),
            Decimal: str,
        }
    )

    