from peewee import *
#please refer to: http://docs.peewee-orm.com/en/latest/peewee/models.html
import datetime

db = MySQLDatabase('facedb', user='root', password='root', charset='utf8')

class BaseModel(Model):
    
    class Meta:
        database = db
        
class Image(BaseModel):
    name = CharField()
    path = CharField()
    token = CharField()
    create_time = DateTimeField(default=datetime.datetime.now())
    
if __name__ == "__main__":
    db.create_tables([Image])
    img = Image(name='xfc', path='./1.jpg', token='1323232')
    img.save()