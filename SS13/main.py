from fastapi import FastAPI, Depends, HTTPException, status, Request

from database import get_db, Base, engine
from sqlalchemy import text
from sqlalchemy.orm import Session
from service import get_all_menu, create_dish_ser, get_dish_ser, update_dish_ser, delete_dish_ser, to_dict, success_response, fail_response
from schemas import DishCreate, DishUpdate
from fastapi.exceptions import RequestValidationError


Base.metadata.create_all(bind = engine)

app = FastAPI()

@app.exception_handler(HTTPException)
def http_exception_handler(request:Request, exc: HTTPException):
    return fail_response(
        status_code=exc.status_code,
        message=exc.detail,
        error="Failed!",
        path = request.url.path
    )

@app.exception_handler(Exception)
def global_exception_handler(request:Request, exc: Exception):
    return fail_response(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        message="Loi He Thong",
        error=str(exc),
        path = request.url.path
    )

@app.exception_handler(RequestValidationError)
def validation_exception_handler(request:Request, exc: RequestValidationError):
    return fail_response(
        status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
        message="Du lieu dau vao khong hop le",
        error=exc.errors(),
        path = request.url.path
    )


@app.get("/connect")
def test_connect(db: Session = Depends(get_db)):
    try:
        db.execute(text("SELECT 1"))
        return {
            "message": "Connected Successful!"
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )


@app.post("/menu-items")
def create_dish(request: Request, new_dish: DishCreate, db: Session = Depends(get_db)):
    dish = create_dish_ser(db=db, dish_code=new_dish.dish_code, dish_n=new_dish)
    return success_response(
                status_code=status.HTTP_200_OK,
                message="Get Documents Successful!",
                data= to_dict(dish),
                error=None,
                path=request.url.path
            )
    

@app.get("/menu-items")
def get_menu_items(request: Request, db: Session = Depends(get_db)):
    result = get_all_menu(db=db)
    return success_response(
            status_code=status.HTTP_200_OK,
            message="Get Documents Successful!",
            data= (to_dict(i) for i in result),
            error=None,
            path=request.url.path
        )

@app.get("/menu-items/{item_id}")
def get_dish(request: Request,item_id: int, db: Session = Depends(get_db)):
    dish = get_dish_ser(item_id=item_id, db=db)
    return success_response(
                status_code=status.HTTP_200_OK,
                message="Get Documents Successful!",
                data= to_dict(dish),
                error=None,
                path=request.url.path
            )

@app.put("/menu-items/{item_id}")
def update_dish(request: Request,item_id: int, dish: DishUpdate, db: Session = Depends(get_db)):
    dish_update = update_dish_ser(db=db, item_id=item_id, dish=dish)
    if not dish_update:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Dish Not Found"
        )
    return success_response(
                    status_code=status.HTTP_200_OK,
                    message="Get Documents Successful!",
                    data= to_dict(dish_update),
                    error=None,
                    path=request.url.path
                )

@app.delete("/menu-items/{item_id}")
def delete_dish(request: Request,item_id: int, db: Session = Depends(get_db)):
    dish = delete_dish_ser(db=db, item_id=item_id)
    if not dish:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Not Found"
        )
    return success_response(
                        status_code=status.HTTP_200_OK,
                        message="Get Documents Successful!",
                        data= to_dict(dish),
                        error=None,
                        path=request.url.path
                    )
