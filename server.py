from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware


from utils.database import DBManip
from utils.validators import  orderActionData
from routes import auth_router, consumer_router, seller_router

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


@app.post("/order_actions")
def orderActions(action: orderActionData):
    db.orderAction(action.id, action.action)
    return {"success": True, "data":True}

@app.get("/order_status/{id}")
def orderStatus(id: str):
    response = db.orderStatus(id=id)
    return {"success": response}