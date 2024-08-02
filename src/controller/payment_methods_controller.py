from fastapi import APIRouter
from fastapi.encoders import jsonable_encoder

from ..dto.payment_methods_input import createManySchema, formatSchema
from ..services.create_payments_service import CreatePaymentMethods

paymentMethods = APIRouter(prefix="/payment-methods")


@paymentMethods.post("/format-methods")
async def formated(body: formatSchema):
    body = jsonable_encoder(body)
    return CreatePaymentMethods().formate_payment_methods(body)


@paymentMethods.post("/payment-methods")
async def create(body: createManySchema):
    body = jsonable_encoder(body)
    return CreatePaymentMethods().createMany(body)