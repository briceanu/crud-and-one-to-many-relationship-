from database.db_connection import get_db
from .blogs_model import Blog , Blog_pydantic_response, Blog_pydantic_save
from users.user_model import User
from fastapi import APIRouter, Depends, Body, status
from sqlalchemy.orm import Session
from typing import Annotated
from fastapi.exceptions import HTTPException
import uuid
from datetime import datetime


router = APIRouter(prefix='/blog', tags=['routing for the blogs'])

@router.post('/create_blog')
async def create_blog(
    blog:Annotated[Blog_pydantic_save,Body()],
    session:Session = Depends(get_db),
    )  -> Blog_pydantic_response:
    try:
        blog = Blog(**blog.dict())
        session.add(blog)
        session.commit()
        session.refresh(blog)
        return blog
    except Exception as e:
        raise HTTPException(status_code=500,detail=f'an error occured: {str(e)}')
    finally:
        session.close()





"""list all blogs"""
@router.get('/list_blogs', description="lists all blogs")
async def list_blogs_of_user(
    session:Session = Depends(get_db),
    )  -> list[Blog_pydantic_response]:
    try:
        blogs = session.query(Blog).all()
        return blogs
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")
    




"""list a single blog"""
@router.get('/list_blog/{user_id}', description="gets all the blogs of a user based on its uuid.")
async def list_blogs_of_user(
    user_id:Annotated[str,uuid],
    session:Session = Depends(get_db),
    )  -> list[Blog_pydantic_response]:
    try:

        user_uuid = uuid.UUID(user_id)
        blogs = session.query(Blog).filter(Blog.user_id == user_uuid).all()
        return blogs
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid UUID format")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")
    


@router.delete('/remove_blog')
async def remove_blog(
    blog_uuid_param:Annotated[str,uuid],
    session:Session=Depends(get_db)) -> dict:
    try:
        blog_uuid = uuid.UUID(blog_uuid_param)
        blog = session.get(Blog, blog_uuid) 
        if blog is None:
            raise HTTPException(status_code=400,detail=f'no blog with the id: {blog_uuid} found.')
        session.delete(blog)
        session.commit()
        return {'status':status.HTTP_204_NO_CONTENT,'success':f'blog with the id {blog_uuid} removed.'}

    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid UUID format")
    except Exception as e:
        session.rollback()
        raise HTTPException(status_code=500, detail=f'An error occured: {str(e)}')
    finally:
        session.close()



@router.patch('/update_blog')
async def update_blog(
    blog_query_uuid:Annotated[str,uuid],
    new_description:Annotated[str,Body()]=None,
    session:Session = Depends(get_db))-> Blog_pydantic_response:
    try:

        validated_uuid = uuid.UUID(blog_query_uuid)
        blog = session.get(Blog,validated_uuid)
        if blog is None:
            raise HTTPException(status_code=400, detail=f'no blog with the id {blog_query_uuid} found.')
        blog.description = new_description
        blog.date_of_publish = datetime.now()
        session.commit()
        session.refresh(blog)
        return blog

    except ValueError :
        raise HTTPException(status_code=400,detail=f'Invalid UUID format')
    except HTTPException:  
        raise

    except Exception as e:
        session.rollback()
        raise HTTPException(status_code=500,detail=f'an error occured {str(e)}')
    finally:
        session.close()

        