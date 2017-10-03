import os

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "django_project.settings")

from django.core.wsgi import get_wsgi_application

application = get_wsgi_application()

from urllib import request, parse
from termcolor import colored
import urllib
import re
from waterlooworks.models import Job
from decimal import Decimal
from async_promises import Promise
import time
import threading


def error_log(message):
    print(colored(message, 'red'))


def check_company_name(company_name):
    company_name = '+'.join(company_name.split())
    return company_name


def get_stoke_price(company_name):
    google_finance_result = str(urllib.request.urlopen(
        "https://www.google.ca/finance?q=" + check_company_name(company_name)).read())
    if 'no matches' in google_finance_result:
        return "-1"
    elif 'Related companies' in google_finance_result:
        try:
            return Decimal(
                re.search(r'class\=\"pr\"[\w\W]+?\>(.+?)\<\/span\>', google_finance_result).group(1).replace(',', ''))
        except Exception:
            return "0"
    else:
        try:
            return Decimal(
                re.search(r'\<th[\w\W]+?Company[\w\W]+?<td class\=\"price rgt nwp\"\>[\w\W]+?\>(.+?)<\/span\>',
                          google_finance_result).group(1).replace(',', ''))
        except Exception:
            return "0"


def get_job_promise(job):
    def action(resolve, reject):
        try:
            print("Attemping To Get " + job.organization)
            job.organization_price = get_stoke_price(job.organization)
            print(str(job.fake_id) + " - " + job.organization + " Got")
            job.save()
        except Exception as e:
            error_log(e)

    while threading.active_count() > 200:
        time.sleep(2)

    success = False
    while success is False:
        try:
            p = Promise(action)
            success = True
        except Exception:
            time.sleep(2)
            success = False

    return p


all_job_promise = [get_job_promise(job) for job in Job.objects.filter(organization_price="")]
