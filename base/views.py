#Import necessary libraries
import pickle
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.shortcuts import render
import numpy as np
import joblib



# Create your views here.
@api_view(['GET'])
def index_page(request):
    return_data = {
        "error" : "0",
        "message" : "Successful",
    }
    return Response(return_data)



@api_view(["POST"])
def predict_malware(request):
    try:
        # machine = request.data.get('Machine',None)
        ds = request.data.get('DebugSize',None)
        dr = request.data.get('DebugRVA',None)
        miv = request.data.get('MajorImageVersion',None)
        mov = request.data.get('MajorOSVersion',None)
        er = request.data.get('ExportRVA',None)
        es = request.data.get('ExportSize',None)
        iv = request.data.get('IatVRA',None)
        malv = request.data.get('MajorLinkerVersion',None)
        milv = request.data.get('MinorLinkerVersion',None)
        nos = request.data.get('NumberOfSections',None)
        sosr = request.data.get('SizeOfStackReserve',None)
        dllc = request.data.get('DllCharacteristics',None)
        rs = request.data.get('ResourceSize',None)
        btca = request.data.get('BitcoinAddresses',None)

        fields = [ds, dr, miv, mov, er, es, iv, malv, milv, nos, sosr, dllc, rs, btca]
        # print(fields)
        if not None in fields:
            #Datapreprocessing Convert the values to int
            # machine = int(machine)
            ds = int(ds)
            dr = int(dr)
            miv = int(miv)
            mov = int(mov)
            er = int(er)
            es = int(es)
            iv = int(iv)
            malv = int(malv)
            milv = int(milv)
            nos = int(nos)
            sosr = int(sosr)
            dllc = int(dllc)
            rs = int(rs)
            btca = int(btca)

            result = [[ds, dr, miv, mov, er, es, iv, malv, milv, nos, sosr, dllc, rs, btca]]
            result = np.array(result).reshape((1,-1))

            #Passing data to model & loading the model from disks
            print('got to the classifier')
            classifier = joblib.load('base/xgb_model.pkl') 
            
            print('got here...')
            prediction = classifier.predict(result)
            predictions = {
                # 'error' : '0',
                # 'message' : 'Successfull',
                'prediction' : prediction
            }
        else:
            predictions = {
                'error' : '1',
                'message': 'Invalid Parameters'                
            }
    except Exception as e:
        predictions = {
            'error' : '2',
            "message": str(e)
        }

    return Response(predictions)

import requests


import os
import hashlib
import math
import array
import pefile
import yara
from termcolor import colored
import colorama
import pandas as pd

# Function get md5 calculates the md5 hash of a given file.
# def get_md5(file):
    
#     # Note that sometimes you won't be able to fit the whole file in memory.
#     # In that case, you'll have to read chunks of 4096 bytes
#     # sequentially and feed them to the Md5 function:
#     # https://stackoverflow.com/questions/3431825/generating-an-md5-checksum-of-a-file



from django.http.response import JsonResponse
from rest_framework.parsers import JSONParser 
from rest_framework import status
 
from base.models import Tutorial
from base.serializer import TutorialSerializer
from rest_framework.decorators import api_view

from collections import OrderedDict
from collections import Counter



@api_view(['GET', 'POST', 'DELETE'])
def threats_list(request):
    #  return render(request, 'index.html') 
    # GET list of threats, POST a new tutorial, DELETE all tutorials
    if request.method == 'GET':
        tutorials = Tutorial.objects.all()
        
        filename = request.GET.get('filename', None)
        if filename is not None:
            tutorials = tutorials.filter(title__icontains=filename)
        
        tutorials_serializer = TutorialSerializer(tutorials, many=True)
        # return JsonResponse(tutorials_serializer.data, safe=False)
        # print("Tutorial serializer", tutorials_serializer.data)
        my_dict = tutorials_serializer.data
        print("Tutorial serializer", my_dict)
        context = []
        print(context)


        for key in my_dict:
            context.append(key['prediction'])


        counts = Counter(context)
        threats = counts['1']
        print(threats)

                

        # print('context', context)
        return render(
        request,
        'index.html', 
        {
            'tutorials_serializer': tutorials_serializer.data, 
            'threats': threats,
        }
    )
    # elif request.method == 'POST':
    #     tutorial_data = JSONParser().parse(request)
    #     tutorial_serializer = TutorialSerializer(data=tutorial_data)
    #     if tutorial_serializer.is_valid():
    #         tutorial_serializer.save()
    #         return JsonResponse(tutorial_serializer.data, status=status.HTTP_201_CREATED) 
    #     return JsonResponse(tutorial_serializer.errors, status=status.HTTP_400_BAD_REQUEST)