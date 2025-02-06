from fastapi import APIRouter, Depends, Body 
from .user_model import User , User_model_pydatic, User_model_pydatic_response, User_model_pydatic_update_name
from database.db_connection import get_db
from sqlalchemy.exc import IntegrityError
from database.db_connection import get_db
from sqlalchemy.orm import Session
from typing import Annotated
from fastapi.exceptions import HTTPException
from fastapi import status
import uuid
router = APIRouter(prefix='/user', tags=['the routing for the users'])




"""create a user """
@router.post('/create_user')
async def create_user(
    user: Annotated[User_model_pydatic,Body()],
    session: Session=Depends(get_db)) -> dict: 
    try:
        user = User(**user.dict())
        session.add(user)
        session.commit()
        return {"status_code":f'{status.HTTP_201_CREATED}', 'message':'user successfully created'}
    except IntegrityError :
        session.rollback()
        raise HTTPException(status_code=400,detail=f'username already exists')
    except Exception as e:
        raise HTTPException(status_code=500,detail=f'an error occured: {str(e)}')
    finally:
        session.close()


"""list all users"""
@router.get('/list_users')
async def create_user(
    session: Session=Depends(get_db)) -> list[User_model_pydatic_response]: 
    try:
        users = session.query(User).all()
        return users
    
    except Exception as e:
        raise HTTPException(status_code=500,detail=f'an error occured: {str(e)}')
    finally:
        session.close()


"""removing an user"""
@router.delete('/remove_user/{user_id}',description='remove an user ')
async def remove_user(
    user_id:Annotated[str,uuid],
    session:Session=Depends(get_db)) -> dict:
    try:
        validated_uuid=uuid.UUID(user_id)
        user = session.get(User,validated_uuid)
        if user is None:
            raise HTTPException(status_code=400,detail=f'no user with the uuid {validated_uuid} found.')
        session.delete(user)
        session.commit()
        return {'status_code':status.HTTP_204_NO_CONTENT, "success":f'user with the id {validated_uuid} removed.'}
    except HTTPException:
        raise
    except ValueError:
        raise HTTPException(status_code=400, detail='Invalid uuid provided.')
    except Exception as e:
        session.rollback()
        raise HTTPException(status_code=500, detail=f'an error occured: {str(e)}')
    finally:
        session.close()
    

"""update a user using the put method"""
@router.put('/update_user')
async def update_user(
    user_data:Annotated[User_model_pydatic,Body()],
    user_id:Annotated[str,uuid],
    session:Session=Depends(get_db)) -> User_model_pydatic_response:
    try:
        valid_uuid = uuid.UUID(user_id)
        user = session.get(User,valid_uuid)
        if user is None:
            raise HTTPException(status_code=400,detail=f'no user with the uuid {valid_uuid} found.')
        user.username = user_data.username
        user.date_of_birth = user_data.date_of_birth
        session.commit()
        session.refresh(user)
        return user
    except HTTPException:
        raise
    except IntegrityError:
        raise HTTPException(status_code=400, detail=f'user name already exists')
    except Exception as e:
        session.rollback()
        raise HTTPException(status_code=500,detail=f'an error occured: {str(e)}')
    finally:
        session.close()


"""updating the name of the user"""
@router.patch('/update_name')
async def update_new_username(
    userdata:User_model_pydatic_update_name,
    user_id:Annotated[str,uuid],
    session:Session=Depends(get_db),
    ):
    try:
        valid_uuid=uuid.UUID(user_id)
        user = session.get(User,valid_uuid)
        if user is None:
            raise HTTPException(status_code=400,detail=f'no user with the uuid {valid_uuid} found.')
        user.username = userdata.username
        session.commit()
        session.refresh(user)
        return {'status_code':status.HTTP_200_OK, 'success':user}

    except ValueError:
        raise HTTPException(status_code=400, detail='Invalid uuid format')
    except HTTPException:
        raise
    except IntegrityError:
        raise HTTPException(status_code=400, detail=f'user name already exists')
    except Exception as e:
        session.rollback()
        raise HTTPException(status_code=500,detail=f'an error occured: {str(e)}')
    finally:
        session.close()