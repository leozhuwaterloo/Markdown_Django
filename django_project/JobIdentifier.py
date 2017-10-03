import os

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "django_project.settings")

from django.core.wsgi import get_wsgi_application

application = get_wsgi_application()

from http import cookiejar
from urllib import request, parse
from termcolor import colored
import urllib
import re
from django.core.validators import URLValidator
from django.core.validators import ValidationError
from waterlooworks.models import Job
from async_promises import Promise
import threading
import time
from googleapiclient.discovery import build

cj = cookiejar.CookieJar()
opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(cj))
urllib.request.install_opener(opener)


def error_log(message):
    print(colored(message, 'red'))


def exists(path):
    try:
        req = urllib.request.Request(path, headers={'User-Agent': 'Chrome'})
        urllib.request.urlopen(req).read()
    except Exception:
        return False

    return True


def get_root(path):
    return re.search(r'(.+?\:\/\/.+?)\/', path).group(1)


def get_company_icon_url(job):
    company_name = job.organization
    time.sleep(1)
    # print(company_name)
    company_url = ""
    try:
        print("Attempting to get " + company_name)
        service = build("customsearch", "v1", developerKey="AIzaSyA6pJksHfPA9T6LrI0X1Hg3YHXeJKkKjIc")
        results = service.cse().list(
            q=company_name,
            cx='015115731645511862899:a5yftjbitis',
            num='1',
            gl='ca'
        ).execute()
        company_url = results['items'][0]['link']
        job.job_website_url = results['items'][0]['displayLink']
        # print(company_url)
    except Exception as e:
        error_log(company_name + " - Unable To Find Its Website - " + str(e))
        return

    try:
        company_page_req = urllib.request.Request(company_url, headers={'User-Agent': 'Chrome'})
        company_page_content = urllib.request.urlopen(company_page_req).read()
    except Exception as e:
        error_log(company_name + " - Error Getting To Its Website - " + str(e))
        return
    # print(company_icon_page_content)

    try:
        company_icon_url = re.search(
            r'<link[^\>]+?rel\=\"[^\>\"]*?icon[^\>\"]*?\"[^>]+?href\=\"([^\>\"]+?)\"[^\>]*?\>',
            str(company_page_content)).group(1)
    except Exception:
        try:
            company_icon_url = re.search(
                r'<link[^\>]+?href\=\"([^\>\"]+?)\"[^\>]+?rel\=\"[^\>\"]*?icon[^\>\"]*?\"[^>]*?\>',
                str(company_page_content)).group(1)
        except Exception:
            error_log(company_name + " - Unable To Find Icon, Trying '/favicon.ico'")
            company_icon_url = "/favicon.ico"

    if company_icon_url[0] == '/':
        # print(company_url)
        company_url = get_root(company_url)

    val = URLValidator()
    try:
        val(company_icon_url)
    except ValidationError:
        company_icon_url = company_url + company_icon_url

    try:
        val(company_icon_url)
    except ValidationError:
        error_log(company_name + " - Icon Not Found")
        return

    if exists(company_icon_url):
        return company_icon_url
    else:
        error_log(company_icon_url + " - Icon Does Not Exist")
        return


for job in Job.objects.all():
    if job.job_website_url == "":
        job.job_icon_url = get_company_icon_url(job)
        job.save()
        print(job.organization + " Process Finished")
