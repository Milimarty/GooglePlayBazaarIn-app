import datetime
import traceback
import requests
from google_bazaar_payment import models

from google_bazaar_payment.payment.utils import logger
from google_bazaar_payment.payment.payment_data import BazaarData, GoogleData
from django.conf import settings


class GBPayment:
    # refresh_token = None
    # expires_in = None
    # access_token = None
    # init_token = None
    payment_data = None

    access_url = ''
    init_url = ''
    validate_url = ""
    _payment_type = 0

    def __checker(self):
        if self.__check_token():
            return self.__check_expired_time()
        return False

    def __check_token(self):
        logger("Checking token")
        if self.payment_data.refresh_token is None:

            logger("token is ", self.payment_data.refresh_token)
            payment_obj = models.Payment.objects.filter(type=self._payment_type).all()
            logger(payment_obj[0])
            if len(payment_obj) > 0 and payment_obj[0].refresh_token is not None and len(
                    payment_obj[0].refresh_token) > 0:
                logger(payment_obj[0])
                self.payment_data.refresh_token = payment_obj[0].refresh_token
                self.payment_data.expires_in = payment_obj[0].expires_in
                self.payment_data.access_token = payment_obj[0].access_token
                self.payment_data.init_token = payment_obj[0].init_token
                return True
            else:
                return self.__get_init_token()
        else:
            return True

    def __check_expired_time(self):
        now = datetime.datetime.timestamp(datetime.datetime.now())
        if now < self.payment_data.expires_in:
            return True
        else:
            return self.__get_access_token()

    def __get_access_token(self):
        try:
            init_token = models.Payment.objects.filter(type=self._payment_type).get()
            self.payment_data.init_token = init_token.init_token
            self.payment_data.client_id = init_token.client_id
            self.payment_data.client_secret = init_token.client_secret
            data = {
                'grant_type': 'refresh_token',
                'client_id': init_token.client_id,
                'client_secret': init_token.client_secret,
                'refresh_token': init_token.refresh_token,
            }
            response = requests.post(self.access_url, data)
            if response.status_code == 200:
                response_data = response.json()
                init_token.access_token = response_data['access_token']
                init_token.token_type = response_data['token_type']
                now = datetime.datetime.timestamp(datetime.datetime.now())
                init_token.expires_in = (now + response_data['expires_in'])
                init_token.scope = response_data['scope']
                self.payment_data.access_token = response_data['access_token']
                self.payment_data.expires_in = (now + response_data['expires_in'])
                logger("expires_in= ", self.payment_data.expires_in)
                init_token.type = self._payment_type
                init_token.save()
                return True
            else:
                logger(response.text)
                return False
        except:
            traceback.print_exc()
            return False

    def __get_init_token(self):
        try:
            init_token = models.Payment.objects.filter(type=self._payment_type).get()
            self.payment_data.client_id = init_token.client_id
            self.payment_data.client_secret = init_token.client_secret
            self.payment_data.init_token = init_token.init_token
            data = {
                'grant_type': 'authorization_code',
                'code': init_token.init_token,
                'client_id': init_token.client_id,
                'client_secret': init_token.client_secret,
                'redirect_uri': init_token.redirect_url,
            }
            logger(data)
            logger("init" * 35)
            response = requests.post(self.init_url, data)
            if response.status_code == 200:
                response_data = response.json()
                init_token.access_token = response_data['access_token']
                init_token.refresh_token = response_data['refresh_token']
                init_token.token_type = response_data['token_type']
                now = datetime.datetime.timestamp(datetime.datetime.now())
                init_token.expires_in = (now + response_data['expires_in'])
                init_token.scope = response_data['scope']
                self.payment_data.refresh_token = response_data['refresh_token']
                self.payment_data.access_token = response_data['access_token']
                self.payment_data.expires_in = (now + response_data['expires_in'])
                init_token.type = self._payment_type
                init_token.save()
                return True
            else:
                logger(response.text)
                return False
        except:
            traceback.print_exc()
            return False

    def check_purchased_token(self, token, product_id, *args, **kwargs):

        """
        :var type = 0 is GOOGLE PLAY
        :var type = 1 is BAZAAR 
        """
        _payment_type = kwargs["type"]
        if _payment_type == 0:
            self.payment_data = GoogleData()
            self.access_url = f'https://accounts.google.com/o/oauth2/token'
            self.init_url = f'https://accounts.google.com/o/oauth2/token'
            validate_url = f'https://androidpublisher.googleapis.com/androidpublisher/v3/applications/{settings.GOOGLE_BUNDLE_ID}/purchases/products/{product_id}/tokens/{token} '
        else:
            self.payment_data = BazaarData()
            self.access_url = 'https://pardakht.cafebazaar.ir/devapi/v2/auth/token/'
            self.init_url = 'https://pardakht.cafebazaar.ir/devapi/v2/auth/token/'
            validate_url = f'https://pardakht.cafebazaar.ir/devapi/v2/api/validate/{settings.BAZAAR_BUNDLE_ID}/inapp/{product_id}/purchases/{token}/?access_token={self.payment_data.access_token}'

        logger("inside check")
        logger("Client_id", self.payment_data.client_id)
        logger("client_secret", self.payment_data.client_secret)
        logger("init_token", self.payment_data.init_token)

        logger("access_token =", self.payment_data.access_token, "refresh_token", self.payment_data.refresh_token)

        if self.__checker():
            logger("access_token =", self.payment_data.access_token, "refresh_token", self.payment_data.refresh_token)

            logger("inside check", "-" * 35)
            if _payment_type == 0:
                response = requests.get(validate_url,
                                        headers={"Authorization": f"Bearer {self.payment_data.access_token}"})
            else:
                response = requests.get(validate_url)

            if response.status_code == 200:
                response_data = response.json()
                if response_data['purchaseState'] == 0:
                    return True
            else:
                logger(response.text)
                return False
        return False


bazaar_payment_method = GBPayment()
