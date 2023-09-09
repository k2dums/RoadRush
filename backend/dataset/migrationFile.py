from django.db import migrations
import json
from django.contrib.gis.geos import fromstr
from pathlib import Path
from authentication.models import User
import math
import random
from psycopg2 import errors
from psycopg2._psycopg import IntegrityError
from itertools import permutations

DATA_FILENAMES=['arunachal.json','sikkim.json','delhi.json']
CAR_MODELS=[" Maruti Suzuki Celerio","Hyundai Santro","Maruti Suzuki Wagon R","Tata Tiago","Hyundai Xcent","Maruti Suzuki Ciaz","Maruti Suzuki Dzire","Honda Amaze","Maruti Alto"]
def load_data(apps,schema_editor):
    UniqueViolation = errors.lookup('23505')
    Driver=apps.get_model('driver','Driver')
    number=6000
    permlist=list(permutations('wxyz'))
    pernumber=0
    for fileno,DATA_FILENAME in enumerate (DATA_FILENAMES):
        perfix=None
        if fileno==0:
            prefix='AR'
        elif fileno==1:
            prefix='SK'
        else:
            prefix='DELHI'
        jsonfile=Path(__file__).parents[2]/"dataset"/DATA_FILENAME
        with open(str(jsonfile),encoding="utf8") as datafile:
            objects = json.load(datafile)
            for obj in objects['elements']:
                try:
                    objType = obj['type']
                    if objType == 'node':
                        tags = obj['tags']
                        username = tags.get('name','no-name')#name can be spaced and repeated
                        username=username.split(" ")
                        username="_".join(username)+f"{prefix}{pernumber}"
                        pernumber=pernumber+1
                        email=username+"@gmail.com"
                        password='12345'
                        carId=number
                        carModel=CAR_MODELS[math.floor(random.random()*(len(CAR_MODELS)))]
                        carNumber=f'{math.floor(random.random()*999)} {math.floor(random.random()*999)} {math.floor(random.random()*999)}'
                        longitude = obj.get('lon', 0)
                        latitude = obj.get('lat', 0)
                        number=number+1
                        location = fromstr(f'POINT({longitude} {latitude})', srid=4326)
                        Driver(username=username,email=email,password=password,carId=carId,carModel=carModel,carNumber=carNumber,location=location,type=User.UserTypes.DRIVER).save()
                except KeyError:
                    pass



class Migration(migrations.Migration):

    dependencies = [
        
    ]


    
    operations = [
        migrations.RunPython(load_data)
    ] 