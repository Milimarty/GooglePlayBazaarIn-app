# Google Play and Bazaar in-app purchase

This Django app created to check the response token that is taken from Google Play or Bazaar is valid or not. and choice with the method you want to confirm your purchase with that.




### STEP 1
#### Install
1. pip install django-google-bazaar-payment
2. pip install requests
3. Add "google_bazaar_payment" to your INSTALLED_APPS setting like this:
```python
    INSTALLED_APPS = [
        ...
        'google_bazaar_payment',
    ]
```
4. Run ``python manage.py migrate`` to create the google_bazaar_payment models






### STEP 2
#### Google Play  Implementation
1. you must add ``GOOGLE_BUNDLE_ID`` to your project settings like this:
```python
	GOOGLE_BUNDLE_ID = "com.package.android"
```
2. Go to Django admin panel and in the payment section add a new record with information that you got from this link: [Authorization](https://developers.google.com/android-publisher/authorization)
4. Set the field type in the record you created to `` Google Play `` 
5. init token in record is the first token and initializer token that you took from the top link and this will use just one time .





### STEP 3  **For Bazaar Users**
#### Bazaar Implementation
1. you must add ``BAZAAR_BUNDLE_ID`` to your project settings like this:
```python
	BAZAAR_BUNDLE_ID = "com.package.android"
```
2. Go to Django admin panel and in the payment section add a new record with information that you got from this link : [Authorization](https://developers.cafebazaar.ir/fa/docs/developer-api-v2-introduction/developer-api-v2-getting-started/)
4. Set the field type in the record you created to `` Bazaar ``
5. init token in record is the first token and initializer token that you took from the top link and this will use just one time. .



### STEP 4 How to use

``` python
from google_bazaar_payment.payment.google_bazaar_payment import GBPayment

result = GBPayment.check_purchased_token(token="token that you received from server", product_id="product_id", type=0)
# type = 0 google play
# type = 1 Bazaar
if result:
    print("token is valid")
else:
    print("token is not valid OR there is an error if you get error you will see it in logs")


```

```
Copyright 2020 MiladNalbandi

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
```



