import base64
import uuid
from flask import Flask,request,Response,json,jsonify
app = Flask(__name__)
@app.route('/authstub1')
def authstub1():
    # name = request.args.get('na','aa')
    # return f'Hello,{name}!'
    if 'Authorization' in request.headers:
        basicAuth = request.headers['Authorization']
        res = basicAuth.split("Basic ", 1)
        splitString = res[1]
        #------ for decoding
        base64_bytes = splitString.encode("ascii")
        sample_string_bytes = base64.b64decode(base64_bytes)
        sample_string = sample_string_bytes.decode("ascii")
        #-----------for seperating uname and pwd
        array = sample_string.split(":")
        user_dic = {"navee": "aaaa", "akhil": "abcd"} 
        custno_dic = {"navee": "1234", "akhil": "2222"} 
        if array[0] in user_dic.keys():
            if (user_dic[array[0]] == array[1]) == True :
                # uid = uuid.uuid1()
                # head = f'confirmation_code: {uid}'
                # # Response.headers.set('confirmation_code', uid)
                # resp = '{"response": "uname found and matched with pwd","confirmation_code":"' + str(uid) + '"}'
                resp = '{"customerNo":"' + custno_dic[array[0]]  + '"}'
                return Response(response= resp, status=200, mimetype='application/json')
                
            else:
                return Response(response='{"response": "user found but password incorrect"}', status=401, mimetype='application/json')
        else :
            # status_code = 401;
            # message='user not found'
            return Response(response='{"response": "user not found"}', status=401, mimetype='application/json')
            #return f'Hello,{array}.......{user_dic[array[0]] == array[1]}!'
    return Response(response='{"response": "Authorization header not found"}', status=401, mimetype='application/json')
app.run()

# response should be 200ok with confirmation code