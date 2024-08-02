from fastapi import FastAPI
from .controller.payment_methods_controller import paymentMethods

app = FastAPI()

app.include_router(paymentMethods)