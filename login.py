from flask import Flask, render_template, redirect,request,Response,url_for,jsonify,json,session
import base64,requests
import random, string, uuid, time,oracledb
from datetime import datetime

login = Flask(__name__)
login.secret_key = 'uwyfewueyfiwu'
@login.route('/login')
def index():
    session['consentId']=request.args.get("consentId")
    
    # originalUrl=request.args.get('original-url')
    
    session['originalUrl']=request.args.get('original-url')
    

    return render_template('login.html')

@login.route('/consent',methods=['POST'])
def consent():
    try:
        consentId=session['consentId']
        originalUrl=session['originalUrl']
        # originalUrl=request.args.get('original-url')
        loc ='original-url=' + originalUrl
        selected_account = request.form.get("account")
        consent = request.form.get("consent")
        username = session['username']
        customerNo=session['customerNo']
        updation_time=session['updation_time']
        session.pop('consentId', None)
        session.pop('originalUrl', None)
        session.pop('customerNo', None)
        session.pop('username', None)
        session.pop('updation_time',None)
        if consent == "allow":
            confirmation_code = str(uuid.uuid1())
            db_insert(consentId,username,customerNo,selected_account,updation_time,confirmation_code)
            if(len(confirmation_code) > 0 and len(username) > 0):

                loc  = loc + '&confirmation=' + confirmation_code + '&username=' + username
            return Response(response=loc,headers= {"Location":loc}, status=200, mimetype='application/json')
            
        elif consent == "cancel":
            return jsonify({'error': 'Consent denied'}), 500
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    

    


@login.route('/login_get', methods=['POST'])
def login():
    # Render the HTML login page
    # loc=''
    try:
        consentId=session['consentId']
        # originalUrl=session['originalUrl']
        # # originalUrl=request.args.get('original-url')
        # loc = loc +'original-url=' + originalUrl
        if request.method == "POST":
            username=request.form.get("username")
            session['username']=username
            password=request.form.get("password")
            base64basic=username + ':' + password
            string_bytes = base64basic.encode("ascii")
            base64_bytes = base64.b64encode(string_bytes)
            base64_string = base64_bytes.decode("ascii")
            basicAuth = "Basic " + base64_string
            headers= {"Authorization":basicAuth, "consentId":consentId}
            # params={"original-url":originalUrl}
            customerNumberResp = requests.get('http://localhost:5000/authstub1',headers=headers)
            if customerNumberResp.status_code == 200 :
                if(customerNumberResp.text):
                    customerNumberResp_json = json.loads(customerNumberResp.text)
                    customerNo = customerNumberResp_json['customerNo']
                    session['customerNo']=customerNo
                    customerNoheaders= {'customerNo':customerNo}
                    customerDetailsResp = requests.get('http://localhost:5001/authstub2',headers=customerNoheaders)
                    if customerDetailsResp.status_code == 200 :
                        if (customerDetailsResp.text) :
                            customerDetails = json.loads(customerDetailsResp.text)
                            updation_time = datetime.now()
                            session['updation_time']=updation_time
                            valid = isConsentExpired(consentId,updation_time)
            
                            if (valid == 'valid') :
                                
                                return render_template('consent.html',accounts=json.loads(customerDetails))
                            else:
                                return jsonify({'error': valid}), 500
                    else:
                        return jsonify({'error': str(customerDetailsResp.text)}), customerDetailsResp.status_code
                else :
                    return jsonify({'error': 'Customer number response body not found'}), 500
            else :
                return jsonify({'error': str(customerNumberResp.text)}), customerNumberResp.status_code
    except Exception as e:
        return jsonify({'error': str(e)}), 500




        ###########################################db############################
        
# def db_insert(consentId,username,customerNo,selected_account,updation_time,confirmation_code):
    
#     # updation_timestamp = datetime.now()
#     conn = oracledb.connect(user="system", password="naveena1998", host="localhost", port="1521", service_name="orcl")
#     cursor = conn.cursor()
#     # insert_sql = "INSERT INTO CONSNET_DETAILS (CONSENT_ID, CUSTOMER_NUMBER, ACCOUNT_NUMBER, VALIDITY, CREATION_TIME, UPDATION_TIME) VALUES (:1, :2, :3, :4, :5, :6)"
#     # cursor.execute(insert_sql, (consentId, customerNo, selected_account, validity, current_timestamp, current_timestamp))
#     update_sql= "UPDATE CONSNET_DETAILS SET USER_NAME = :1, CUSTOMER_NUMBER = :2, ACCOUNT_NUMBER = :3, UPDATION_TIME=:4, CONFIRMATION_CODE=:5 WHERE CONSENT_ID=:6"
#     cursor.execute(update_sql, (username, customerNo, selected_account,updation_time,confirmation_code, consentId))

#     conn.commit()

#     if cursor:
#         cursor.close()

#     if conn:
#         conn.close()
# def isConsentExpired(consentId,updation_time):
#     select_sql = "SELECT VALIDITY,CREATION_TIME FROM CONSNET_DETAILS WHERE CONSENT_ID = :CONSENT_ID"
   
#     params={'CONSENT_ID':consentId}
#     # select_sql = "SELECT * FROM CONSNET_DETAILS"
#     conn = oracledb.connect(user="system", password="naveena1998", host="localhost", port="1521", service_name="orcl")
#     cursor = conn.cursor()
#     # cursor = conn.cursor()
#     cursor.execute(select_sql,(params))
    
#     row=cursor.fetchone()
#     conn.commit()
#     if cursor:
#         cursor.close()

#     if conn:
#         conn.close()
#     if(row):
#         validity=int(row[0])
        
#         creation_time=datetime.strftime(row[1],'%Y-%m-%d %H:%M:%S')
#         # updation_time=updation_timestamp
#         # updation_time=datetime.strftime(updation_timestamp,'%Y-%m-%d %H:%M:%S')
    
    
#         ts1 = row[1].timestamp()
#         ts2=updation_time.timestamp()

#         difference=ts2-ts1
        
#         if difference <= validity :
#             print(valid)
#             return 'valid'
        
#         else :
#             return 'not valid'
#     else:
#         return 'consent details missing'
         

#         # redirect_url = "http://localhost:5002/authorization?original-url="+originalUrl
#         # customerDetailsResp = requests.get(redirect_url,headers=headers)
#         # # response.headers["Authorization"]=basicAuth
#         # # # response.headers["consentId"]=consentId
#         # # # response.args["original-url"]=originalUrl
#         # # return response
#         # # print(response.text)
#         # # print(response.status_code)
#         # return Response(response=customerDetailsResp.text, status=200, mimetype='application/json')
#         # print(base64_string)

#     # return render_template('login.html')


################################## db stub #############################################
def db_insert(consentId,username,customerNo,selected_account,updation_time,confirmation_code):
    return
    # updation_timestamp = datetime.now()
    # conn = oracledb.connect(user="system", password="naveena1998", host="localhost", port="1521", service_name="orcl")
    # cursor = conn.cursor()
    # # insert_sql = "INSERT INTO CONSNET_DETAILS (CONSENT_ID, CUSTOMER_NUMBER, ACCOUNT_NUMBER, VALIDITY, CREATION_TIME, UPDATION_TIME) VALUES (:1, :2, :3, :4, :5, :6)"
    # # cursor.execute(insert_sql, (consentId, customerNo, selected_account, validity, current_timestamp, current_timestamp))
    # update_sql= "UPDATE CONSNET_DETAILS SET USER_NAME = :1, CUSTOMER_NUMBER = :2, ACCOUNT_NUMBER = :3, UPDATION_TIME=:4, CONFIRMATION_CODE=:5 WHERE CONSENT_ID=:6"
    # cursor.execute(update_sql, (username, customerNo, selected_account,updation_time,confirmation_code, consentId))

    # conn.commit()

    # if cursor:
    #     cursor.close()

    # if conn:
    #     conn.close()
def isConsentExpired(consentId,updation_time):
    if (consentId=='2') :
        return 'valid'
    else :
        return 'not valid'

         

        # redirect_url = "http://localhost:5002/authorization?original-url="+originalUrl
        # customerDetailsResp = requests.get(redirect_url,headers=headers)
        # # response.headers["Authorization"]=basicAuth
        # # # response.headers["consentId"]=consentId
        # # # response.args["original-url"]=originalUrl
        # # return response
        # # print(response.text)
        # # print(response.status_code)
        # return Response(response=customerDetailsResp.text, status=200, mimetype='application/json')
        # print(base64_string)

    # return render_template('login.html')

if __name__ == '__main__':
    # app.run(debug=False,host='localhost',port=5004)
    login.run()
