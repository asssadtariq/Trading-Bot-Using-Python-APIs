import requests
import json

class Bot():
    def __init__(self, id, p_pass, api_k):
        self.identifier = id
        self.password = p_pass
        self.api_key = api_k
        self.CST = ""
        self.X_SECURITY_TOKEN = ""

    def make_connection(self):
        headers = {
            "X-CAP-API-KEY": self.api_key,
            "Content-Type": "application/json",
        }

        data = {
            "encryptedPassword": "false",
            "identifier": self.identifier,
            "password": self.password,
        }

        # Using demo api links for testing purposes
        response = requests.post('https://demo-api-capital.backend-capital.com/api/v1/session',
                                 headers=headers, data=json.dumps(data))

        if response.status_code == 200:
            self.CST = response.headers['CST']
            self.X_SECURITY_TOKEN = response.headers['X-SECURITY-TOKEN']

        return response.status_code

    def make_trade(self, data_dict):

        headers = {
            "X-SECURITY-TOKEN": self.X_SECURITY_TOKEN,
            "CST": self.CST,
            "Content-Type": "application/json"
        }

        # Using demo api links for testing purposes
        response = requests.get('https://demo-api-capital.backend-capital.com/api/v1/markets/' + data_dict['epic'],
                                headers=headers)
        
        if response.status_code == 200:
            response_data = response.content
            response_data = response_data.decode()
            
            new_dict = json.loads(response_data)
            minSize = new_dict['dealingRules']['minDealSize']['value']

            if minSize > int(data_dict['size']):
                return -1

            headers = {
                "X-SECURITY-TOKEN": self.X_SECURITY_TOKEN,
                "CST": self.CST,
                "Content-Type": "application/json"
            }

            data = {
                "direction": data_dict['direction'],
                "epic": data_dict['epic'],
                "size": int(data_dict['size']),
                "stopDistance": float(data_dict['stopDistance']),
                "limitDistance": float(data_dict['limitDistance'])
            }

            response = requests.post('https://demo-api-capital.backend-capital.com/api/v1/positions',
                headers=headers, data=json.dumps(data))

            return response.status_code

        return response.status_code
