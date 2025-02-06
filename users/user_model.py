from sqlalchemy.orm import Mapped , mapped_column, validates, relationship
from database.db_connection import Base
from sqlalchemy import String , Date
import uuid
from datetime import date
from pydantic import Field, BaseModel, field_validator
from blogs.blogs_model import Blog

 


class User(Base):
    __tablename__ = 'user_table'

    user_id : Mapped[uuid.UUID] = mapped_column(default=lambda:uuid.uuid4(), primary_key=True)
    username : Mapped[str] = mapped_column(String(50),nullable=False,unique=True)
    date_of_birth: Mapped[date] = mapped_column(Date(),nullable=False)
    blogs: Mapped[list["Blog"]] = relationship( back_populates="user", cascade="all, delete")
  
 
    """  user_id, username, date_of_birth  """

    @validates
    def validate_date_of_birth(self,key,value):
        min_date = date(1930,1,1)
        if value < min_date:
            raise ValueError("Date of birth cannot be earlier than 01-01-1930")
        return value

 

################################################################################################7

class User_model_pydatic(BaseModel):
    """  user_id, username, date_of_birth, age  """

    username :str = Field(max_length=50, unique=True)
    date_of_birth : date = Field()

    @field_validator('date_of_birth')
    @classmethod
    def validate_date_of_birth(cls,value):
        min_date = date(1930,1,1)
        if value < min_date:
            raise ValueError("Date of birth cannot be earlier than 01-01-1930")
        return value


    class Config:
        from_attributes=True
        extra = 'forbid'

  


class User_model_pydatic_response(User_model_pydatic):
    user_id: uuid.UUID



class User_model_pydatic_update_name(BaseModel):
    username :str = Field(max_length=50, unique=True)
  
    class Config:
        from_attributes=True
        extra = 'forbid'


 