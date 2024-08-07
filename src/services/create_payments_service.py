import os
import logging
from requests import request
import json
from dotenv import load_dotenv
from ..dto.payment_methods_input import createManySchema, formatSchema


load_dotenv()

class CreatePaymentMethods:
    
    def __init__(self) -> None:
        self.url_configuration = os.getenv("URL_CONFIGURATION")
    
    def format_payment_methods_payretails(self, body: formatSchema):
        form = body["form"]
        id_country = body["id_country"]
        id_pay_type = body["id_pay_type"]
        
        data = body['data']
        formatedData = []

        for item in data:
            newData = {}
            newData["name"] = item["name"]
            newData["code"] = item['paymentMethodId']
            newData["url_image"] = item["imageUrl"]
            newData["form"] = form
            newData["id_country"] = id_country
            newData["id_pay_type"] = id_pay_type

            formatedData.append(newData)
        
        return {
            "success": True,
            "payload": formatedData
        }

    def formate_payment_methods(self, body: formatSchema):
        form = body["form"]
        id_country = body["id_country"]
        id_pay_type = body["id_pay_type"]
        
        data = body['data']
        formatedData = []
        
        for item in data:
            newData = {}
            newData["name"] = item["name"]
            newData["code"] = f"{item['uid']}-{item['channel']}"
            newData["url_image"] = item["imageUrl"]
            newData["form"] = form
            newData["id_country"] = id_country
            newData["id_pay_type"] = id_pay_type

            formatedData.append(newData)
        
        return {
            "success": True,
            "payload": formatedData
        }
    

    def createMany(self, body: createManySchema):
        
        try:
            id_psp = body['id_psp']
            endpoint = body['endpoint']
            paymentMethods = body['paymentMethods']
            
            url = self.url_configuration
            
            headers = {
                "accept": "application/json",
                "Content-Type": "application/json"
            }
            
            methods_success =[]
            
            for method in paymentMethods:
                
                payload = {}
                payload['id_psp'] = id_psp
                payload['name'] = method['name']
                payload['code'] = method['code'] 
                payload['url_image'] = method['url_image']
                payload['form'] = method['form']
                payload['id_country'] = method['id_country']
                payload['id_pay_type'] = method['id_pay_type'] 
                payload['config'] = {}
                
                try:
                    ## Insert payment method
                    response = request("POST", f"{url}/payment_methods/create", headers=headers, data=json.dumps(payload, indent=4))
                    
                    if not response.status_code == 200:
                        logging.warning(response.status_code)
                        logging.warning("NOT SUCCESS: {}".format(str(response.text)))
                    else:
                        ## Insert endpoint
                        idPaymentMethod = response.json()['payload']['id']

                        urlEnpoint = "{}/psp_transaction/create/endpoint".format(url)
                        payload = {}
                        payload["idPaymentMethod"] = idPaymentMethod
                        payload["endpoint"] = endpoint
                        
                        method_response = {}
                        method_response['name'] = method['name']
                        method_response["paymentMethod"] = True
                        method_response["endpoint"] = False

                        try:
                            endpoint_response = request("POST", urlEnpoint, headers=headers, data=json.dumps(payload, indent=4))
                            
                            if not endpoint_response.status_code == 200:
                                logging.warning(endpoint_response.status_code)
                                logging.warning("NOT SUCCESS: {}".format(str(endpoint_response.text)))
                            else:
                                method_response["endpoint"] = True

                        except Exception as err:
                            logging.warning("ERROR ENDPOINT: {}".format(str(err)))

                        methods_success.append(method_response)


                except Exception as err:
                    logging.warning("ERROR: {}".format(str(err)))
                
            
            return {
                "success": True,
                "data": methods_success
            }
        
        except:
            return {
                "success": False,
                "message": "Error"
            }