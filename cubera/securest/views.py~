from django.shortcuts import render


from rest_framework.decorators import api_view
from securest import models as m
from rest_framework.response import Response
from securest.serializers import CustomersSerializer #Used for REST API
from rest_framework import status
from django.contrib.auth.decorators import login_required
from securest import constants
import json, requests, sys, random
import googlemaps #https://github.com/googlemaps/google-maps-services-python
from django.contrib.auth.models import User
from django.db import connection
#from django.core.serializers import serialize

def get_pocket_info(request, account_number):
    #Get the balance
    customer = m.Customers.objects.get(contact=request.user.username)
    data_dict = {
        "id_type" : "TOKEN",
        "id_value" : customer.auth_data,
        "auth_type": "TOKEN",
        "auth_data": customer.auth_data,
        "clientID":"test@abc.com",
        "authToken":"f5316a5e35a4" 
    } 
    response = requests.post(constants.check_balance_url , json=data_dict, timeout=5)
    balance = json.loads(response.content)
    return balance['amount']
    
@api_view(['POST'])
@login_required
def sign_up(request):
    try:
        if request.method == 'POST':
            #Initializing content positively
            content = {
                'status' : 1,
                'response_code' : status.HTTP_200_OK,
                'message' : 'Sign Up successful'
            }
            data_list = []
            loadedJsonData = json.loads(request.body)
            username = checkNone(loadedJsonData.get('mobile'))
            password = checkNone(loadedJsonData.get('password'))
            confirm_password = checkNone(loadedJsonData.get('confirm_password'))
            if password != confirm_password:
                content = {
                    'status' : 1,
                    'response_code' : status.HTTP_400_BAD_REQUEST,
                    'message' : 'Passwords does not match'
                }
                return Response(content)
            email = checkNone(loadedJsonData.get('email'))
            first_name = checkNone(loadedJsonData.get('first_name'))
            last_name = checkNone(loadedJsonData.get('last_name'))
            try:
               phone = int(checkNone(loadedJsonData.get('mobile')))
            except Exception as e:
               print e
               content = {
                    'status' : 0,
                    'response_code' : status.HTTP_400_BAD_REQUEST,
                    'message' : 'Mobile number should be all digits'
                }
               return Response(content)
            '''address1 = checkNone(loadedJsonData.get('address1'))
            address2 = checkNone(loadedJsonData.get('address2'))
            city = checkNone(loadedJsonData.get('city'))
            state = checkNone(loadedJsonData.get('state'))
            country = checkNone(loadedJsonData.get('country'))
            zipcode = checkNone(loadedJsonData.get('zipcode'))
            dob = checkNone(loadedJsonData.get('dob'))
            sex = checkNone(loadedJsonData.get('sex'))
            '''
            user_type = checkNone(loadedJsonData.get('user_type'))
            pocket_account_number = checkNone(loadedJsonData.get('pocket_account_number'))
            
            #Hitting ICICI APIs
            create_wallet_url = '''http://alphaiciapi2.mybluemix.net/rest/Wallet/createWallet/cubera_123/create/Kishan/Simha/ksimha@gmail.com/7842133323/1989-07-12/male/10.22.7.74/android/12345/xyz/test@abc.com/f5316a5e35a4'''
            response = requests.get(create_wallet_url , timeout=5)
            createWalletResponse = json.loads(response.content)
            if createWalletResponse['errorDescripttion'] == 'success':
                #pocket_account_number = pocket_info[1]
                #Saving user info
                new_user = User.objects.create_user(username, email, password)
                #new_user.first_name = fname
                #new_user.last_name = lname
                new_user.save()
                
                #Store information in the Customers table
                new_customer = m.Customers(user=new_user)
                new_customer.first_name = first_name
                new_customer.last_name = last_name
                new_customer.email = email
                new_customer.contact = username
                new_customer.pocket_account_number = int(pocket_account_number)
                new_customer.auth_data = createWalletResponse['WalletDetails'][0]['auth_data']
                new_customer.save()
                
                data_list.append({'user_id' : new_user.id})
                content.update({'data' : data_list})
                return Response(content)
            else:
                content = {
                        'status' : 0,
                        'response_code' : status.HTTP_500_INTERNAL_SERVER_ERROR,
                        'message' : 'ICICI API error.'
                    }
                return Response(content)
        else:
            content = {
                    'status' : 0,
                    'response_code' : status.HTTP_400_BAD_REQUEST,
                    'message' : 'Invalid request method. Only POST is allowed.'
                }
            return Response(content)
    except Exception as general_exception:
        print general_exception
        print "Line number : " + str(sys.exc_traceback.tb_lineno)
        #Delete already created records from the DB, if any
        content = {
                    'status' : 0,
                    'response_code' : status.HTTP_500_INTERNAL_SERVER_ERROR,
                    'message' : 'Something went wrong : ' + str(general_exception)
                }
        return Response(content)

@api_view(['POST'])
def sign_in(request):
    try:
        if request.method == 'POST':
            #Initializing content positively
            content = {
                'status' : 1,
                'response_code' : status.HTTP_200_OK,
                'message' : 'Sign In successful'
            }
            if request.user.is_authenticated():
                try:
                    customer = m.Customers.objects.get(contact=request.user.username)
                    balance = get_pocket_info(request, customer.pocket_account_number)
                    customer.pocket_account_balance = balance
                    customer.save()
                    content.update({
                          'balance' : balance,
                          'fname' : customer.first_name,
                          'lname' : customer.last_name,
                          'mobile' : customer.contact,
                          'email' : customer.email,
                          'role' : 'customer'
                      })
                except Exception as m.Customers.DoesNotExist:
                    try:
                        merchant = m.Merchants.objects.get(contact=request.user.username)
                        content.update({
                              'fname' : merchant.first_name,
                              'lname' : merchant.last_name,
                              'mobile' : merchant.contact,
                              'email' : merchant.email,
                              'role' : 'merchant'
                          })
                    except Exception as m.Merchants.DoesNotExist:
                        content.update({
                            'status' : 0,
                            'response_code' : status.HTTP_403_FORBIDDEN,
                            'message' : 'User exists but not properly registered'
                          })
                return Response(content)
            else:
                content = {
                   'status' : 0,
                   'response_code' : status.HTTP_403_FORBIDDEN,
                   'message' : 'Username Password combination is invalid'
                }
                return Response(content)
        else:
            content = {
                    'status' : 0,
                    'response_code' : status.HTTP_400_BAD_REQUEST,
                    'message' : 'Invalid request method. Only POST is allowed.'
                }
            return Response(content)
    except Exception as general_exception:
        print general_exception
        content = {
                    'status' : 0,
                    'response_code' : status.HTTP_500_INTERNAL_SERVER_ERROR,
                    'message' : 'Something went wrong : ' + str(general_exception)
                }
        return Response(content)


@api_view(['POST'])
@login_required
def notify_nearby_merchants(request):
    try:
        if request.method == 'POST':
            #Initializing content positively
            content = {
                'status' : 1,
                'response_code' : status.HTTP_200_OK,
                'message' : 'Nearby merchants notified'
            }
            
            #For push notifications
            headers = {
                'content-type': 'application/json',
                'Application-Mode' : 'SANDBOX',
                'appSecret' : '50badf8c-d24c-41ef-b19f-02c6ee41ad84'
            }
            radius = 500.0 #By default it is 500 meters
            loadedJsonData = json.loads(request.body)
            latitude = float(checkFloat(loadedJsonData.get('latitude')))
            longitude = float(checkFloat(loadedJsonData.get('longitude')))
            radius = float(checkFloat(loadedJsonData.get('radius')))
            amount = float(loadedJsonData.get('radius'))
            rowData = {}
            dataList = []
            #Cursor for executing raw queries
            cursor = connection.cursor()
            try:
                #http://stackoverflow.com/questions/2234204/latitude-longitude-find-nearest-latitude-longitude-complex-sql-or-complex-calc
                distance_q = '''(SQRT(POW(69.1 * (latitude - %s), 2) + POW(69.1 * (%s - longitude) * COS(latitude / 57.3), 2)))*1.60934*1000'''
                query = 'select id, latitude, longitude, ' + str(distance_q) + ' from merchants where ' + str(distance_q) + ' <= %s'
                cursor.execute(query, (str(latitude), str(longitude),str(latitude), str(longitude), str(radius)))
                transaction_id = str(request.user.username) + str(random.randrange(10000, 999999))
                for row in cursor:
                    rowData = {
                        'merchant_id' : row[0],
                        'distance' : row[3]
                        }
                    transaction_request = m.TransactionRequests(nearby_merchant=m.Merchants.objects.get(id=row[0]), transaction_id=transaction_id)
                    transaction_request.distance = row[3]
                    #Send PUSH notification here to the row[0] merchant ID 
                    data = {
                        "message" : {
                                        "alert" : "New disbursement request"    
                                    },
                         "settings":{
                                    "gcm":{
                                        "payload":{
                                        "action": "new_request",
                                        "TxnID": transaction_id,
                                        "amount": amount
                                        }
                                    }
                                }
                        }
                    push_response = requests.post(constants.push_notification_url, json=data, timeout=5, headers=headers)
                    transaction_request.save()
                    #Formatting for uniformity  
                    dataList.append(rowData)
                content.update({'data' : dataList, "transaction_id" : transaction_id, "amount": amount})
            except Exception as general_exception:
                print general_exception
                content = {
                           'status' : 0,
                           'response_code' : status.HTTP_500_INTERNAL_SERVER_ERROR,
                           'message' : 'Something went wrong'
                          }
                return Response(content) #Exception case
            return Response(content) #Success case
        else:
            content = {
                    'status' : 0,
                    'response_code' : status.HTTP_400_BAD_REQUEST,
                    'message' : 'Invalid request method. Only POST is allowed.'
                }
            return Response(content)
    except Exception as general_exception:
        print general_exception
        content = {
                    'status' : 0,
                    'response_code' : status.HTTP_500_INTERNAL_SERVER_ERROR,
                    'message' : 'Something went wrong: ' + str(general_exception)
                }
        return Response(content)

@api_view(['POST'])
@login_required
def accept_request(request):
    try:
        if request.method == 'POST':
            #Initializing content positively
            content = {
                'status' : 1,
                'response_code' : status.HTTP_200_OK,
                'message' : 'Request accepted'
            }
            try:
                loadedJsonData = json.loads(request.body)
                trasaction_id = loadedJsonData.get('transaction_id')
                merchant_obj = m.Merchants.objects.get(user=request.user)
                transaction_request = m.TransactionRequests.objects.get(transaction_id=trasaction_id, nearby_merchant=merchant_obj)
                transaction_request.accepted_by_merchant = True
                transaction_request.save()
            except Exception as general_exception:
                print general_exception
                content = {
                           'status' : 0,
                           'response_code' : status.HTTP_500_INTERNAL_SERVER_ERROR,
                           'message' : 'Something went wrong'
                          }
                return Response(content) #Exception case
            return Response(content) #Success case
        else:
            content = {
                    'status' : 0,
                    'response_code' : status.HTTP_400_BAD_REQUEST,
                    'message' : 'Invalid request method. Only POST is allowed.'
                }
            return Response(content)
    except Exception as general_exception:
        print general_exception
        content = {
                    'status' : 0,
                    'response_code' : status.HTTP_500_INTERNAL_SERVER_ERROR,
                    'message' : 'Something went wrong: ' + str(general_exception)
                }
        return Response(content)


@api_view(['POST'])
@login_required
def get_merchants(request):
    try:
        if request.method == 'POST':
            #Initializing content positively
            content = {
                'status' : 1,
                'response_code' : status.HTTP_200_OK,
                'message' : 'Nearby merchants fetched'
            }
            dataList = []
            row_data = {}
            try:
                loadedJsonData = json.loads(request.body)
                transaction_id = loadedJsonData.get('transaction_id')
                transaction_request = m.TransactionRequests.objects.filter(transaction_id=transaction_id)
                for tr in transaction_request:
                    row_data = {
                        'merchant_id' : tr.nearby_merchant.id,
                        'shop_name' : tr.nearby_merchant.shop_name,
                        'contact1' : tr.nearby_merchant.contact1,
                        'latitude' : tr.nearby_merchant.latitude,
                        'longitude' : tr.nearby_merchant.longitude,
                        'building_number' : tr.nearby_merchant.shop_address.building_number,
                        'street' : tr.nearby_merchant.shop_address.street,
                        'locality' : tr.nearby_merchant.shop_address.locality,
                        'landmark' : tr.nearby_merchant.shop_address.landmark,
                        'city' : tr.nearby_merchant.shop_address.city,
                        'state' : tr.nearby_merchant.shop_address.state,
                        'country' : tr.nearby_merchant.shop_address.country,
                        'zipcode' : tr.nearby_merchant.shop_address.zipcode,
                        'distance' : tr.distance
                    }
                    dataList.append(row_data)
                content.update({'data' : dataList})
            except Exception as general_exception:
                print general_exception
                content = {
                           'status' : 0,
                           'response_code' : status.HTTP_500_INTERNAL_SERVER_ERROR,
                           'message' : 'Something went wrong'
                          }
                return Response(content) #Exception case
            return Response(content) #Success case
        else:
            content = {
                    'status' : 0,
                    'response_code' : status.HTTP_400_BAD_REQUEST,
                    'message' : 'Invalid request method. Only POST is allowed.'
                }
            return Response(content)
    except Exception as general_exception:
        print general_exception
        content = {
                    'status' : 0,
                    'response_code' : status.HTTP_500_INTERNAL_SERVER_ERROR,
                    'message' : 'Something went wrong: ' + str(general_exception)
                }
        return Response(content)

@api_view(['POST'])
@login_required
def select_merchant(request):
    try:
        if request.method == 'POST':
            #Initializing content positively
            content = {
                'status' : 1,
                'response_code' : status.HTTP_200_OK,
                'message' : 'Merchant selected'
            }
            dataList = []
            loadedJsonData = json.loads(request.body)
            transaction_id = loadedJsonData.get('transaction_id')
            merchant_id = loadedJsonData.get('merchant_id')
            merchant = m.Merchants.objects.get(id=int(merchant_id))
            transaction_request = m.TransactionRequests.objects.get(transaction_id=transaction_id, nearby_merchant=merchant)
            transaction_request.selected_by_customer = True
            #Generate a new OTP
            otp = m.OTPHistory(valid=True, transaction_req=transaction_request)
            otp.save()
            transaction_request.otp = otp
            transaction_request.save()
            data = {'otp' : transaction_request.otp.otp}
            dataList.append(data)
            content.update({'data' : data})
            return Response(content)
        else:
            content = {
                    'status' : 0,
                    'response_code' : status.HTTP_400_BAD_REQUEST,
                    'message' : 'Invalid request method. Only POST is allowed.'
                }
            return Response(content)
    except Exception as general_exception:
        print general_exception
        print "Line number : " + str(sys.exc_traceback.tb_lineno)
        content = {
                    'status' : 0,
                    'response_code' : status.HTTP_500_INTERNAL_SERVER_ERROR,
                    'message' : 'Something went wrong : ' + str(general_exception)
                }
        return Response(content)

@api_view(['POST'])
@login_required
def verify_otp(request):
    try:
        if request.method == 'POST':
            #Initializing content positively
            content = {
                'status' : 1,
                'response_code' : status.HTTP_200_OK,
                'message' : 'OTP verified',
            }
            loadedJsonData = json.loads(request.body)
            transaction_id = loadedJsonData.get('transaction_id')
            merchant_id = loadedJsonData.get('merchant_id')
            otp = loadedJsonData.get('otp')
            merchant = m.Merchants.objects.get(id=int(merchant_id))
            transaction_request = m.TransactionRequests.objects.get(transaction_id=transaction_id, nearby_merchant=merchant)
            otpObj = m.OTPHistory.objects.filter(transaction_req=transaction_request).order_by('-id')[0]
            if (otpObj.otp == int(otp)):
                return Response(content)
            else:
                content = {
                    'status' : 0,
                    'response_code' : status.HTTP_400_BAD_REQUEST,
                    'message' : 'OTP not verified',
                }
                return Response(content)
        else:
            content = {
                    'status' : 0,
                    'response_code' : status.HTTP_400_BAD_REQUEST,
                    'message' : 'Invalid request method. Only POST is allowed.'
                }
            return Response(content)
    except Exception as general_exception:
        print general_exception
        content = {
                    'status' : 0,
                    'response_code' : status.HTTP_500_INTERNAL_SERVER_ERROR,
                    'message' : 'Something went wrong : ' + str(general_exception)
                }
        return Response(content)

@api_view(['POST'])
@login_required
def rate_merchant(request):
    try:
        if request.method == 'POST':
            #Initializing content positively
            content = {
                'status' : 1,
                'response_code' : status.HTTP_200_OK,
                'message' : 'Rating submitted successfully',
            }
            loadedJsonData = json.loads(request.body)
            transaction_id = loadedJsonData.get('transaction_id')
            transaction = m.TransactionRequests.objects.get(transaction_id=int(transaction_id))
            merchant_id = loadedJsonData.get('merchant_id')
            merchant = m.Merchants.objects.get(id=int(merchant_id))
            star_rating = loadedJsonData.get('star_rating')
            reviewObj = m.Reviews(transaction_req=transaction, merchant=merchant, star_rating=star_rating, user=request.user)
            reviewObj.save()
            return Response(content)
        else:
            content = {
                    'status' : 0,
                    'response_code' : status.HTTP_400_BAD_REQUEST,
                    'message' : 'Invalid request method. Only POST is allowed.'
                }
            return Response(content)
    except Exception as general_exception:
        print general_exception
        content = {
                    'status' : 0,
                    'response_code' : status.HTTP_500_INTERNAL_SERVER_ERROR,
                    'message' : 'Something went wrong : ' + str(general_exception)
                }
        return Response(content)

@api_view(['POST'])
@login_required
def credit(request):
    try:
        if request.method == 'POST':
            #Initializing content positively
            content = {
                'status' : 1,
                'response_code' : status.HTTP_200_OK,
                'message' : 'Amount credited successfully',
            }
            loadedJsonData = json.loads(request.body)
            transaction_id = loadedJsonData.get('transaction_id')
            merchant_id = loadedJsonData.get('merchant_id')
            amount = loadedJsonData.get('amount')
            merchant = m.Merchants.objects.get(id=int(merchant_id))
            merchant.balance = checkFloat(merchant.balance) + float(amount)
            merchant.save()
            transaction_request = m.TransactionRequests.objects.get(transaction_id=transaction_id, nearby_merchant=merchant)
            transaction_request.credit_to_merchant = True
            transaction_request.save()
            return Response(content)
        else:
            content = {
                    'status' : 0,
                    'response_code' : status.HTTP_400_BAD_REQUEST,
                    'message' : 'Invalid request method. Only POST is allowed.'
                }
            return Response(content)
    except Exception as general_exception:
        print general_exception
        print "Line number : " + str(sys.exc_traceback.tb_lineno)
        content = {
                    'status' : 0,
                    'response_code' : status.HTTP_500_INTERNAL_SERVER_ERROR,
                    'message' : 'Something went wrong : ' + str(general_exception)
                }
        return Response(content)

@api_view(['POST'])
@login_required
def debit(request):
    try:
        if request.method == 'POST':
            #Initializing content positively
            content = {
                'status' : 1,
                'response_code' : status.HTTP_200_OK,
                'message' : 'Amount Debited successfully'
            }
            loadedJsonData = json.loads(request.body)
            amount = loadedJsonData.get('amount')
            transaction_id = loadedJsonData.get('transaction_id')
            merchant_id = loadedJsonData.get('merchant_id')
            customer = m.Customers.objects.get(user=request.user)
            
            data_dict = {
                "id_type" : "TOKEN",
                "id_value" : customer.auth_data,
                "auth_type" : "TOKEN",
                "auth_data" : customer.auth_data,
                "txn_id": "123498",
                "amount": amount,
                "clientID":"test@abc.com",
                "authToken":"f5316a5e35a4"
            }
            response = requests.post(constants.debit_url , json=data_dict, timeout=5)
            debit_response = json.loads(response.content)
            if debit_response["errorDescripttion"] == "Insufficient Balance":
                content = {
                    'status' : 0,
                    'response_code' : status.HTTP_400_BAD_REQUEST,
                    'message' : 'Insufficient Balance'
                }
                return Response(content)
            balance_after_debit = debit_response["amount"]
            if debit_response["errorDescripttion"] == "success":
                #Debiting in the CUbera's DB
                customer.pocket_account_balance = customer.pocket_account_balance - float(amount)
                customer.save()
                merchant = m.Merchants.objects.get(id=int(merchant_id))
                transaction_request = m.TransactionRequests.objects.get(transaction_id=transaction_id, nearby_merchant=merchant)
                transaction_request.debited_from_customer = True
                transaction_request.save()
            content.update({'balance_after_debit' : balance_after_debit})
            return Response(content)
        else:
            content = {
                    'status' : 0,
                    'response_code' : status.HTTP_400_BAD_REQUEST,
                    'message' : 'Invalid request method. Only POST is allowed.'
                }
            return Response(content)
    except Exception as general_exception:
        print general_exception
        print "Line number : " + str(sys.exc_traceback.tb_lineno)
        content = {
                    'status' : 0,
                    'response_code' : status.HTTP_500_INTERNAL_SERVER_ERROR,
                    'message' : 'Something went wrong : ' + str(general_exception)
                }
        return Response(content)


def checkNone(objectToCheck):
    if objectToCheck is None:
        return ''
    else:
        return objectToCheck

def checkFloat(objectToCheck):
    if objectToCheck is None:
        return 0.0
    else:
        return objectToCheck

def checkInt(objectToCheck):
    if objectToCheck is None:
        return 0
    else:
        return objectToCheck
