from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column , relationship
 
from  database.db_connection import Base
import uuid
from datetime import datetime 
from pydantic import BaseModel 

class Blog(Base):
    __tablename__ = 'blog'

    blog_id: Mapped[uuid.UUID] = mapped_column(default=lambda: uuid.uuid4(), primary_key=True, nullable=False)
    description: Mapped[str] = mapped_column(String, nullable=False)  
    date_of_publish: Mapped[datetime] = mapped_column(default=datetime.now()) 
    user_id: Mapped[uuid.UUID] = mapped_column(ForeignKey('user_table.user_id'))
    user: Mapped["User"] = relationship(back_populates="blogs")

 
class Blog_pydantic_save(BaseModel):
    description: str
    user_id: uuid.UUID


class Blog_pydantic_response(Blog_pydantic_save):
    date_of_publish: datetime
    blog_id :uuid.UUID

