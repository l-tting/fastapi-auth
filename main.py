from fastapi import FastAPI,Depends,status,HTTPException
from sqlalchemy.orm import Session
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import schemas,database,models,services,auth
from datetime import timedelta

app = FastAPI()


# create tables
models.Base.metadata.create_all(database.engine)

@app.post('/register',response_model=dict,status_code=status.HTTP_201_CREATED)
def register_user(user:schemas.UserRegister,db:Session=Depends(database.get_db)):
    existing_user = db.query(models.User).filter(models.User.email == user.email).first()
    if existing_user:
        raise HTTPException(status_code=400,detail="User already exists,please login")
    hashed_password = services.generate_password_hash(user.password)
    new_user = models.User(
        full_name = user.full_name,
        username=user.username,
        email = user.email,
        password = hashed_password
        )
    db.add(new_user)
    db.commit()
    # update and sync with database state
    db.refresh(new_user)
    return {"Message":"User created successfully"}


@app.post('/login',status_code=status.HTTP_201_CREATED)
def login_user(user:schemas.UserLogin,db:Session= Depends(database.get_db)):
    registered_user = db.query(models.User).filter(models.User.email==user.email).first()
    if registered_user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="User not found,please register")
    try:
        verify_user_password = services.check_password_hash(user.password,registered_user.password)
        if verify_user_password:
            access_token = auth.create_access_token(data={"user":user.email},expires_delta=timedelta(minutes=10))
            refresh_token = auth.create_refresh_token(data={"user":user.email},expires_delta=timedelta(days=2))
            response = JSONResponse(content={"message":"Login successful"})

            response.set_cookie(
                key="access_token",
                value = access_token,
                httponly=True,
                secure=False,
                max_age=3600
            )
            response.set_cookie(
                key="refresh_token",
                value=refresh_token,
                httponly=True,
                secure=False,
                max_age=3600
            )
            return response
        
    except Exception as error:
        raise HTTPException(status_code=500,detail=f'Error creating token: {error}')
