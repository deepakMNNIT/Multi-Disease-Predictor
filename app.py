from flask import Flask, render_template, request, flash, redirect
import pickle
import numpy as np
from PIL import Image
from tensorflow.keras.models import load_model
import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'
from py_files.database import engine, db_session
import py_files.schema
import json

app = Flask(__name__)

def init():
    global connection, cursor
    connection = engine.raw_connection()
    cursor = connection.cursor()

def predict(values, dic):
    if len(values) == 8:
        model = pickle.load(open('models/diabetes.pkl','rb'))
        values = np.asarray(values)
        return model.predict(values.reshape(1, -1))[0]
    elif len(values) == 26:
        model = pickle.load(open('models/breast_cancer.pkl','rb'))
        values = np.asarray(values)
        return model.predict(values.reshape(1, -1))[0]
    elif len(values) == 13:
        model = pickle.load(open('models/heart1.pkl','rb'))
        values = np.asarray(values)
        return model.predict(values.reshape(1, -1))[0]
    elif len(values) == 18:
        model = pickle.load(open('models/kidney.pkl','rb'))
        values = np.asarray(values)
        return model.predict(values.reshape(1, -1))[0]
    elif len(values) == 10:
        model = pickle.load(open('models/liver.pkl','rb'))
        values = np.asarray(values)
        return model.predict(values.reshape(1, -1))[0]

def predict_proba(values, dic):
    if len(values) == 8:
        model = pickle.load(open('models/diabetes.pkl','rb'))
        values = np.asarray(values)
        positive_percent= model.predict_proba(values.reshape(1, -1))[0][1]*100
        return positive_percent
    elif len(values) == 26:
        model = pickle.load(open('models/breast_cancer.pkl','rb'))
        values = np.asarray(values)
        positive_percent= model.predict_proba(values.reshape(1, -1))[0][1]*100
        return positive_percent
    elif len(values) == 13:
        model = pickle.load(open('models/heart1.pkl','rb'))
        values = np.asarray(values)
        positive_percent= model.predict_proba(values.reshape(1, -1))[0][1]*100
        return positive_percent
    elif len(values) == 18:
        model = pickle.load(open('models/kidney1.pkl','rb'))
        values = np.asarray(values)
        positive_percent= model.predict_proba(values.reshape(1, -1))[0][1]*100
        return positive_percent
    elif len(values) == 10:
        model = pickle.load(open('models/liver1.pkl','rb'))
        values = np.asarray(values)
        positive_percent= model.predict_proba(values.reshape(1, -1))[0][1]*100
        return positive_percent

    
@app.route("/")
def home():
    return render_template('home.html')

@app.route("/diabetes", methods=['GET', 'POST'])
def diabetesPage():
    return render_template('diabetes.html')

@app.route("/cancer", methods=['GET', 'POST'])
def cancerPage():
    return render_template('breast_cancer.html')

@app.route("/heart", methods=['GET', 'POST'])
def heartPage():
    return render_template('heart.html')

@app.route("/kidney", methods=['GET', 'POST'])
def kidneyPage():
    return render_template('kidney.html')

@app.route("/liver", methods=['GET', 'POST'])
def liverPage():
    return render_template('liver.html')

@app.route("/malaria", methods=['GET', 'POST'])
def malariaPage():
    return render_template('malaria.html')

@app.route("/pneumonia", methods=['GET', 'POST'])
def pneumoniaPage():
    return render_template('pneumonia.html')

@app.route("/get_history", methods = ['POST', 'GET'])
def get_history_data():
    return render_template('get_history.html')

@app.route("/predict", methods = ['POST', 'GET'])
def predictPage():
    # try:
        if request.method == 'POST':
            to_predict_dict1 = request.form.to_dict()
            # print(to_predict_dict1)
            
            to_predict_list1 = list(map(float, list(to_predict_dict1.values())))
            # print(to_predict_list1)
            if len(to_predict_list1) == 9:
                pat_id = str(to_predict_dict1['patientid']) 
                to_predict_dict2 = {}
                to_predict_dict2['pregnancies'] = int(to_predict_list1[8])
                to_predict_dict2['glucose'] = to_predict_list1[4]
                to_predict_dict2['bloodpressure'] = to_predict_list1[3]
                to_predict_dict2['skinthickness'] = to_predict_list1[7]
                to_predict_dict2['insulin'] = to_predict_list1[5]
                to_predict_dict2['bmi'] = to_predict_list1[2]
                to_predict_dict2['dpf'] = to_predict_list1[6]
                to_predict_dict2['age'] = int(to_predict_list1[1])
            else :
                to_predict_dict2 = to_predict_dict1
                
            # to_predict_dict = to_predict_dict1
            # to_predict_list = to_predict_list1
           
            # if len(to_predict_list) == 9:
                
            #     to_predict_list.pop(0)
                
                
            to_predict_list2 = list(map(float, list(to_predict_dict2.values())))    
            # print(to_predict_dict2)
            # print(to_predict_list2)

            pred = predict(to_predict_list2, to_predict_dict2)
            a = predict_proba(to_predict_list2, to_predict_dict2)
            res = ''
            conf_score = ''
            if(pred == 1):
                res = 'positive'
            else:
                res = 'negative'
            conf_score = str(a)
            c = a
            result = ''
            if len(to_predict_list2) == 8:
                conf_score1 = int(float(conf_score))
                
                if(conf_score1 < 50):
                    conf_score1 = 50
                if(conf_score1 > 50 and conf_score1 <= 60):
                    conf_score1 = 60
                elif(conf_score1 > 60 and conf_score1 <= 80):
                    conf_score1 = 80
                elif(conf_score1 > 80 and conf_score1 <= 100):
                    conf_score1 = 100
                # elif(conf_score1 > 65 and conf_score1 <= 70):
                #     conf_score1 = 70
                # elif(conf_score1 > 70 and conf_score1 <= 75):
                #     conf_score1 = 75
                # elif(conf_score1 > 75 and conf_score1 <= 80):
                #     conf_score1 = 80
                # elif(conf_score1 > 80 and conf_score1 <= 85):
                #     conf_score1 = 85
                # elif(conf_score1 > 85 and conf_score1 <= 90):
                #     conf_score1 = 90
                # elif(conf_score1 > 90 and conf_score1 <= 95):
                #     conf_score1 = 95
                # elif(conf_score1 > 95 and conf_score1 <= 100):
                #     conf_score1 = 100
                 
                conf_score2 = str(conf_score1)
                qr_string = '''query($conf : String!){
                                  allProcedures(conf: $conf){
                                    edges{
                                      node{
                                        conf,
                                        procedure
                                    }
                                    }
                                  }
                                }'''
                qr_result = py_files.schema.schema.execute(qr_string,variables={
                                                    'conf' : conf_score2
                                            },)
                dt_q = json.dumps(qr_result.data)
                dt_q = json.loads(dt_q)
                dat = str(dt_q)
                res1 = dat[dat.find("'procedure':")+14 : ]
                result = res1[ : res1.find("'")]
                
                mut_string = '''mutation ($patientid : String!, $numberofpregnancies : Int!, $glucose : String!, $bloodpressure : String!, $skinthickness : String!, $insulinlevel : String!, $bodymassindex : String!, $diabetespedigreefunction : String!, $age : Int!, $result : String!, $conf : String!, $procedure : String!){
                        addDiab(patientid : $patientid, numberofpregnancies : $numberofpregnancies, glucose : $glucose, bloodpressure : $bloodpressure, skinthickness : $skinthickness, insulinlevel : $insulinlevel, bodymassindex : $bodymassindex, diabetespedigreefunction : $diabetespedigreefunction, age : $age, result : $result, conf : $conf, procedure : $procedure) {
                            post{
                                patientid,
                                numberofpregnancies,
                                glucose,
                                bloodpressure,
                                skinthickness,
                                insulinlevel,
                                bodymassindex,
                                diabetespedigreefunction,
                                age,
                                result,
                                conf,
                                procedure
                            }
                        }
                    }
                    '''
                fin_result = py_files.schema.schema.execute(mut_string,variables={
                                        'patientid' : pat_id,
                                        'numberofpregnancies': int(to_predict_dict2['pregnancies']),
                                        'glucose' : str(to_predict_dict2['glucose']),
                                        'bloodpressure' : str(to_predict_dict2['bloodpressure']),
                                        'skinthickness' : str(to_predict_dict2['skinthickness']),
                                        'insulinlevel' : str(to_predict_dict2['insulin']),
                                        'bodymassindex' : str(to_predict_dict2['bmi']),
                                        'diabetespedigreefunction' : str(to_predict_dict2['dpf']),
                                        'age' : int(to_predict_dict2['age']),
                                        'result' : res,
                                        'conf': c,
                                        'procedure' : result
                                    
                                },)
                
                
                dt = json.dumps(fin_result.data)
                dt = json.loads(dt)
                
              # result = 
            
            # if len(to_predict_list) == 10:
            #     mut_string = '''mutation ($patientid : String!, $age : Int!, $totalbilirubin : String!, $directbilirubin : String!, $alkalinephosphotase : String!, $alamineaminotransferase : String!, $aspartateaminotransferase : String!, $totalprotiens : String!, $albumin : String!, $albuminandglobulinratio : String!, $gender : String!, $result : String!, $conf : String!){
            #             addLiv(patientid : $patientid, age : $age, totalbilirubin : $totalbilirubin, directbilirubin : $directbilirubin, alkalinephosphotase : $alkalinephosphotase, alamineaminotransferase : $alamineaminotransferase, aspartateaminotransferase : $aspartateaminotransferase, totalprotiens : $totalprotiens, albumin : $albumin, albuminandglobulinratio : $albuminandglobulinratio, gender : $gender, result : $result, conf : $conf) {
            #                 post{
            #                     patientid,
            #                     age,
            #                     totalbilirubin,
            #                     directbilirubin,
            #                     alkalinephosphotase,
            #                     alamineaminotransferase,
            #                     aspartateaminotransferase,
            #                     totalprotiens,
            #                     albumin,
            #                     albuminandglobulinratio,
            #                     gender,
            #                     result,
            #                     conf
            #                 }
            #             }
            #         }
            #         '''
                 
            #     fin_result = py_files.schema.schema.execute(mut_string,variables={
            #                             'patientid' : pat_id,
            #                             'age': int(to_predict_dict['Age']),
            #                             'totalbilirubin' : str(to_predict_dict['Total_Bilirubin']),
            #                             'directbilirubin' : str(to_predict_dict['Direct_Bilirubin']),
            #                             'alkalinephosphotase' : str(to_predict_dict['Alkaline_Phosphotase']),
            #                             'alamineaminotransferase' : str(to_predict_dict['Alamine_Aminotransferase']),
            #                             'aspartateaminotransferase' : str(to_predict_dict['Aspartate_Aminotransferase']),
            #                             'totalprotiens' : str(to_predict_dict['Total_Protiens']),
            #                             'albumin' : str(to_predict_dict['Albumin']),
            #                             'albuminandglobulinratio' : str(to_predict_dict['Albumin_and_Globulin_Ratio']),
            #                             'gender' : str(to_predict_dict['Gender_Male']),
            #                             'result' : res,
            #                             'conf': conf_score
                                    
            #                     },)
            #     dt = json.dumps(fin_result.data)
            #     dt = json.loads(dt)
            return render_template('predict.html', pred = pred, c = c, result=result)
                
    # except:
    #     message = "Please enter valid Data"
    #     return render_template("home.html", message = message)



@app.route("/malariapredict", methods = ['POST', 'GET'])
def malariapredictPage():
    if request.method == 'POST':
        try:
            if 'image' in request.files:
                img = Image.open(request.files['image'])
                img = img.resize((36,36))
                img = np.asarray(img)
                img = img.reshape((1,36,36,3))
                img = img.astype(np.float64)
                model = load_model("models/malaria.h5")
                pred = np.argmax(model.predict(img)[0])
                positive_percent= model.predict_proba(img)[0][1]*100
        except:
            message = "Please upload an Image"
            return render_template('malaria.html', message = message)
    return render_template('malaria_predict.html', pred = pred, positive_percent=positive_percent)

@app.route("/pneumoniapredict", methods = ['POST', 'GET'])
def pneumoniapredictPage():
    if request.method == 'POST':
        try:
            if 'image' in request.files:
                img = Image.open(request.files['image']).convert('L')
                img = img.resize((36,36))
                img = np.asarray(img)
                img = img.reshape((1,36,36,1))
                img = img / 255.0
                model = load_model("models/pneumonia.h5")
                pred = np.argmax(model.predict(img)[0])
                positive_percent= model.predict_proba(img)[0][1]*100

        except:
            message = "Please upload an Image"
            return render_template('pneumonia.html', message = message)
    return render_template('pneumonia_predict.html', pred = pred, positive_percent=positive_percent)


@app.route("/get_data", methods = ['POST', 'GET'])
def getData():
    if request.method == 'POST':
            a = request.form.to_dict()
            patient_id = str(a['patient_id'])
            d_string = '''query($patientid : String!){
                                  allDiabetes(patientid: $patientid){
                                    edges{
                                      node{
                                        patientid,
                                        result,                                  
                                        conf,
                                        procedure,
                                        lastupdatedat
                                      }
                                    }
                                  }
                                }'''
                                        # numberofpregnancies,
                                        # glucose,
                                        # bloodpressure,
                                        # skinthickness,
                                        # insulinlevel,
                                        # bodymassindex,
                                        # diabetespedigreefunction,
                                        # age,
            # l_string = '''query($patientid : String!){
            #                       allLiver(patientid: $patientid){
            #                         edges{
            #                           node{
            #                             patientid,
            #                             result,
            #                             conf,
            #                             procedure,
            #                             lastupdatedat
            #                         }
            #                         }
            #                       }
            #                     }'''
            #                             # age,
            #                             # totalbilirubin,
            #                             # directbilirubin,
            #                             # alkalinephosphotase,
            #                             # alamineaminotransferase,
            #                             # aspartateaminotransferase,
            #                             # totalprotiens,
            #                             # albumin,
            #                             # albuminandglobulinratio,
            #                             # gender,
            d_result = py_files.schema.schema.execute(d_string,variables={
                                                    'patientid' : patient_id    
                                            },)
            d_dt = json.dumps(d_result.data)
            d_dt = json.loads(d_dt)
            
            return render_template('provide_data.html', d_dt=d_dt)



@app.teardown_appcontext
def shutdown_session(exception=None):
    db_session.remove()

if __name__ == '__main__':
    init()
    # init_db()
    app.run(debug = True)
