#coding=utf-8
from django.shortcuts import  render_to_response
from django.http import HttpResponse
import json
import os
from datetime import datetime
from django.core.servers.basehttp import FileWrapper

def home (request):
    return render_to_response('home.html')

