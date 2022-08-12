import requests
import json
from config import URL_ACTIONS
import logging


class Ozon:
    def __init__(self, client_id, api_key):
        self.client_id = client_id
        self.api_key = api_key

        logging.basicConfig(filename='logs.log',
                            level=logging.DEBUG,
                            format = "%(asctime)s - %(levelname)s - %(funcName)s: %(lineno)d - %(message)s",
                            datefmt='%H:%M:%S',)
        self.logger = logging.getLogger('api_class')

    def get_headers(self):
        headers = {
            'Client-Id': self.client_id,
            'Api-key': self.api_key,
            'Content-Type': 'application/json',
        }
        return headers

    def get_actions(self):
        ''' Получает все акции '''
        try:
            response = requests.get(URL_ACTIONS, headers=self.get_headers())
            self.logger.info(response.json())
            return response.json()
        except Exception as e:
            self.logger.error(e)

    def get_actions_(self):
        ''' Получает условия для добавления товаров в акции "скидка не более 5%"  '''
        promotions = []
        try:
            response = requests.get(URL_ACTIONS, headers=self.get_headers()).json()
            for res in response['result']:
                if res['discount_value'] <= 5 and res['discount_type'] == 'PERCENT' or res['discount_value'] == 0:
                    promotions.append(res)
            self.logger.info(promotions)
            return promotions
        except Exception as e:
            self.logger.error(e)

    def get_candidates(self, action_id):
        ''' Получает все товары доступные для акций  '''
        data = {
                'action_id': action_id,
                'limit': 10,
                'offset': 0
            }
        response = requests.post(f'{URL_ACTIONS}/candidates', headers=self.get_headers(), data=json.dumps(data))
        self.logger.info(response.json())
        return response.json()


    def activate_action(self, get_candidates):
        '''Добавить товары в акции подходящие под условия '''
        response = requests.post(f'{URL_ACTIONS}/products/activate', headers=self.get_headers(),
                                 data=json.dumps(get_candidates))
        self.logger.info(response.json())
        return response.json()

    def deactivate_action(self, action_id, product_ids):
        data = {
            "action_id": action_id,
            "product_ids": product_ids,
        }
        response = requests.post(f'{URL_ACTIONS}/products/deactivate', headers=self.get_headers(),
                                 data=json.dumps(data))
        self.logger.info(response.json())
        return response.json()


