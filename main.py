from fastapi import FastAPI
from blogs.blogs_routing import router as blogs_router
from users.users_routing import router as users_router


app = FastAPI()

app.include_router(blogs_router)
app.include_router(users_router)



