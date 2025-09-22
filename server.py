from fastapi import FastAPI, Depends, status
from fastapi.middleware.cors import CORSMiddleware


from utils.database import DBManip
from utils.validators import  orderActionData
from routes import auth_router, consumer_router, seller_router
from utils.dependencies import verify_request

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
    allow_credentials=True,
)
app.include_router(auth_router)
app.include_router(seller_router)
app.include_router(consumer_router)

db = DBManip()


@app.get("/loading", tags=["Main"])
def accountType(verification = Depends(verify_request)):
    if verification[0] == False:
        if verification[1] == "refresh":
            return status.HTTP_401_UNAUTHORIZED
        elif verification[1] == "login":
            return status.HTTP_400_BAD_REQUEST
        else:
            return status.HTTP_204_NO_CONTENT
        
    return verification[1]["acc_type"]