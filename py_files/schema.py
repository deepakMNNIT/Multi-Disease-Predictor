from py_files.model import Liver as LiverModel
from py_files.model import Diabetes as DiabetesModel
from py_files.model import Diabetes_Procedures as Diabetes_ProceduresModel
from py_files.database import db_session as db
import graphene
from graphene import relay, Int
from graphene_sqlalchemy import SQLAlchemyConnectionField, SQLAlchemyObjectType
import json

class Liver(SQLAlchemyObjectType):
    class Meta:
        model = LiverModel
        interfaces = (relay.Node, )


class Diabetes(SQLAlchemyObjectType):
    class Meta:
        model = DiabetesModel
        interfaces = (relay.Node, )
        
class Diabetes_Procedures(SQLAlchemyObjectType):
    class Meta:
        model = Diabetes_ProceduresModel
        interfaces = (relay.Node, )


class Query(graphene.ObjectType):
    node = relay.Node.Field()
    # if you don't want node and edges : replace SQLAlchemyConnectionField with graphene.List
    all_diabetes = SQLAlchemyConnectionField(Diabetes, patientid=graphene.String())#, providerId=graphene.Int())
    all_liver = SQLAlchemyConnectionField(Liver, patientid=graphene.String())#, sort=Provider_Review.sort_argument())
    all_procedures = SQLAlchemyConnectionField(Diabetes_Procedures, conf=graphene.String())
#    def resolve_all_providers(self, info, **args):
#      query = Provider.get_query(info)
#      providerId = args.get('providerId')
#      return query.filter(ProviderModel.provider_id == providerId).all()
    
    def resolve_all_diabetes(self, info, **args):
      query = Diabetes.get_query(info)
      patientid = args.get('patientid')
      return query.filter(DiabetesModel.patientid == patientid).all()
  
    def resolve_all_liver(self, info, **args):
      query = Liver.get_query(info)
      patientid = args.get('patientid')
      return query.filter(LiverModel.patientid == patientid).all()
    
    def resolve_all_procedures(self, info, **args):
      query = Diabetes_Procedures.get_query(info)
      conf = args.get('conf')
      return query.filter(Diabetes_ProceduresModel.conf == conf).all()

class AddDiabetes(graphene.Mutation):
    class Arguments:
        patientid = graphene.String(required=True)
        numberofpregnancies = graphene.Int(required=True)
        glucose = graphene.String(required=True)
        bloodpressure = graphene.String(required=True)
        skinthickness = graphene.String(required=True)
        insulinlevel = graphene.String(required=True)
        bodymassindex = graphene.String(required=True)
        diabetespedigreefunction = graphene.String(required=True)
        age = graphene.Int(required=True)
        result = graphene.String(required=True)
        conf = graphene.String(required=True)
        procedure = graphene.String(required=True)
        
    post = graphene.Field(lambda: Diabetes)
    def mutate(self, info, patientid, numberofpregnancies, glucose, bloodpressure, skinthickness, insulinlevel, bodymassindex, diabetespedigreefunction, age, result, conf, procedure):
        #user = User.query.filter_by(username=username).first()
        post = DiabetesModel(patientid=patientid, numberofpregnancies=numberofpregnancies, glucose=glucose, bloodpressure=bloodpressure, skinthickness=skinthickness, insulinlevel=insulinlevel, bodymassindex=bodymassindex, diabetespedigreefunction=diabetespedigreefunction, age=age, result=result, conf=conf, procedure=procedure)
        db.add(post)
        db.commit()
        return AddDiabetes(post=post)
    
    
class AddLiver(graphene.Mutation):
    class Arguments:
        patientid = graphene.String(required=True)
        age = graphene.Int(required=True)
        totalbilirubin = graphene.String(required=True)
        directbilirubin = graphene.String(required=True)
        alkalinephosphotase = graphene.String(required=True)
        alamineaminotransferase = graphene.String(required=True)
        aspartateaminotransferase = graphene.String(required=True)
        totalprotiens = graphene.String(required=True)
        albumin = graphene.String(required=True)
        albuminandglobulinratio = graphene.String(required=True)
        gender = graphene.String(required=True)
        result = graphene.String(required=True)
        conf = graphene.String(required=True)
        
    post = graphene.Field(lambda: Liver)
    def mutate(self, info, patientid, age, totalbilirubin, directbilirubin, alkalinephosphotase, alamineaminotransferase, aspartateaminotransferase, totalprotiens, albumin, albuminandglobulinratio, gender, result, conf):
        #user = User.query.filter_by(username=username).first()
        post = LiverModel(patientid=patientid, age=age, totalbilirubin=totalbilirubin, directbilirubin=directbilirubin, alkalinephosphotase=alkalinephosphotase, alamineaminotransferase=alamineaminotransferase, aspartateaminotransferase=aspartateaminotransferase, totalprotiens=totalprotiens, albumin=albumin, albuminandglobulinratio=albuminandglobulinratio, gender=gender, result=result, conf=conf)
        db.add(post)
        db.commit()
        return AddLiver(post=post)
    
class Mutation(graphene.ObjectType):
    add_diab = AddDiabetes.Field()
    add_liv = AddLiver.Field()
    
schema = graphene.Schema(query=Query, mutation=Mutation, types=[Diabetes, Liver])

# d_string = '''query($patientid : String!){
#                                   allDiabetes(patientid: $patientid){
#                                     edges{
#                                       node{
#                                         patientid,
#                                         result,
#                                         conf,
#                                         procedure,
#                                         lastupdatedat
#                                       }
#                                     }
#                                   }
#                                 }'''
# d_result = schema.execute(d_string,variables={
#                                                     'patientid' : '1000'
#                                             },)
# d_dt = json.dumps(d_result.data)
# d_dt = json.loads(d_dt)
# # dat = str(d_dt)
# # # dat1 = dat[dat.find("'edges") : len(dat)-2]    
# # # dat2 = json.dumps(dat1)
# # # dat2 = json.loads(dat2)
# # res1 = dat[dat.find("'procedure':")+14 : ]
# # res = res1[ : res1.find("'")]
# print(d_dt)