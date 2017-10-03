import os

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "django_project.settings")

from django.core.wsgi import get_wsgi_application

application = get_wsgi_application()

from bs4 import BeautifulSoup
import urllib
from http import cookiejar
from urllib import request, parse
import re
from async_promises import Promise
import time
from termcolor import colored
import threading
import os
from waterlooworks.models import *

cj = cookiejar.CookieJar()
opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(cj))
urllib.request.install_opener(opener)

for_my_program_url = "https://waterlooworks.uwaterloo.ca/myAccount/co-op/coop-postings.htm"
target_section = "Viewed"
save_path = 'Jobs/'


# for_my_program_url = "https://waterlooworks.uwaterloo.ca/myAccount/hire-waterloo/other-jobs/jobs-postings.htm"

def clean_up_word(word):
    word = word.replace("\\n", " ")
    word = word.replace("\\r", " ")
    word = word.replace("\\t", " ")
    word = word.replace("\\", " ")
    word = word.replace("\<br\>", "##########")
    word = re.sub("\<.+?\>", " ", word)
    word = word.replace("R xe9sum xe9", "Resume")
    word = word.replace("xa0", " ")
    word = " ".join(word.split())
    return word


good_key_list = ['Work Term:', 'Job - Country:', 'Job - Province / State:', 'Number of Job Openings:', 'ID',
                 'Job Summary:', 'Application Documents Required:', 'Special Job Requirements:', 'Job - City:',
                 'Required Skills:', 'Job Type:', 'Job Category (NOC):', 'Targeted Degrees and Disciplines:', 'Region:',
                 'Job Title:', 'Job Responsibilities:', 'Division:', 'Work Term Duration:', 'Additional Information:',
                 'Job - Address Line One:', 'Job - Postal Code / Zip Code (X#X #X#):', 'Employer Internal Job Number:',
                 'Transportation and Housing:', 'Compensation and Benefits Information:', 'Level:', 'Organization:',
                 'Additional Application Information:', 'Job - Address Line Two:', 'Additional Job Identifiers:',
                 'Job Location (if exact address unknown or multiple locations):']


def get_info(program_info, key_num):
    value = ""
    try:
        value = program_info[good_key_list[key_num]]
    except KeyError:
        value = ""
    return value


def organize_program_info_to_database(program_info):
    try:
        temp_job = Job()
        temp_job.work_term = get_info(program_info, 0)
        temp_job.job_country = get_info(program_info, 1)
        temp_job.job_province_state = get_info(program_info, 2)
        temp_job.number_of_job_openings = get_info(program_info, 3)
        temp_job.fake_id = get_info(program_info, 4)
        temp_job.job_summary = get_info(program_info, 5)
        temp_job.application_documents_required = get_info(program_info, 6)
        temp_job.special_job_requirements = get_info(program_info, 7)
        temp_job.job_city = get_info(program_info, 8)
        temp_job.required_skills = get_info(program_info, 9)
        temp_job.job_type = get_info(program_info, 10)
        temp_job.job_Category_noc = get_info(program_info, 11)
        temp_job.targeted_degrees_and_disciplines = get_info(program_info, 12)
        temp_job.region = get_info(program_info, 13)
        temp_job.job_title = get_info(program_info, 14)
        temp_job.job_responsibilities = get_info(program_info, 15)
        temp_job.division = get_info(program_info, 16)
        temp_job.work_Term_duration = get_info(program_info, 17)
        temp_job.additional_information = get_info(program_info, 18)
        temp_job.job_address_line_one = get_info(program_info, 19)
        temp_job.job_postal_code_zip_code_xx_x = get_info(program_info, 20)
        temp_job.employer_internal_job_number = get_info(program_info, 21)
        temp_job.transportation_and_housing = get_info(program_info, 22)
        temp_job.compensation_and_benefits_information = get_info(program_info, 23)
        temp_job.level = get_info(program_info, 24)
        temp_job.organization = get_info(program_info, 25)
        temp_job.additional_application_information = get_info(program_info, 26)
        temp_job.job_address_line_two = get_info(program_info, 27)
        temp_job.additional_Job_identifiers = get_info(program_info, 28)
        temp_job.job_Location_if_exact_address_unknown_or_multiple_locations = get_info(program_info, 29)
        temp_job.save()
        print("Saved " + get_info(program_info, 14))
    except Exception as e:
        error_log(e)


def organize_program_info_to_file(program_info):
    info = ""
    job_title = ""
    job_id = ""
    for key, value in program_info.items():
        info += key + "\t" + value + "\n"
        if key == "Job Title:":
            job_title = value
        elif key == "ID":
            job_id = value

    if job_title == "" or job_id == "":
        error_log("Job Unfound - " + str(program_info))
    else:
        job_title = job_title.replace("/", "")

        if not os.path.exists(save_path):
            os.makedirs(save_path)

        try:
            with open(os.path.join(save_path, job_id + " - " + job_title + ".txt"), 'w', encoding='UTF-8') as f:
                print(job_id + " - " + job_title + '.txt Created')
                f.write(info)
        except Exception as e:
            error_log(e)


def error_log(message):
    print(colored(message, 'red'))


global_counter = 0


def get_program_detail_content_promise(page_counter, counter, link):
    def get_program_detail(resolve, reject):
        program_form_page = urllib.request.urlopen(for_my_program_url + link)
        program_form_content = program_form_page.read()

        # it get another form and we need to submit it
        input_form_data = {}
        input_soup = BeautifulSoup(program_form_content, "html.parser")
        for form_input in input_soup.findAll('input'):
            input_tokens = re.search('\<input name=\"(.*?)\" type=\"hidden\" value\=\"(.*?)\"\/\>',
                                     str(form_input))
            input_form_data[input_tokens.group(1)] = input_tokens.group(2)

        print(str(page_counter * 100 - 100 + counter + 1) + " Acquiring Program Information")
        complete_form_data = urllib.parse.urlencode(input_form_data).encode()
        program_detail_page = urllib.request.urlopen(for_my_program_url, complete_form_data)
        program_detail_content = program_detail_page.read()

        info = {}

        info["ID"] = str(re.search(r"Job ID[\w\W]+?(\d+)", str(program_detail_content)).group(1))
        # print(str(program_detail_content))

        # get rid of td in table
        program_detail_content = re.sub(r'\<td class\=\"\"\>(.+?)\<\/td\>[\w\W]+?\<\/tr\>', r'\g<1>',
                                        str(program_detail_content))

        res = re.findall(
            r'\<tr\>[\w\W]+?\<td style\=\"width\: 25\%\;\"\>(?:[\\rtn]|\<strong\>)+([\w\W]+?)\\[\w\W]+?\<td width=\"75%\"\>(?:[\\rtn]|<strong>)+([\w\W]+?)\<\/tr\>',
            str(program_detail_content))
        for i in res:
            info[clean_up_word(i[0])] = clean_up_word(i[1])
        print(str(page_counter * 100 - 100 + counter + 1) + " Gathered Program Information For " + info['Job Title:'])
        resolve(info)

    return Promise(get_program_detail)


def get_all_page_program_detail_content_promise(program_list_page_token, counter, first_page_content):
    print("Getting Program Lists Promise " + str(counter))

    def get_all_page_program_detail(resolve, reject):
        print("Getting Program Lists " + str(counter))
        if counter != 1:
            selected_program_list_data = urllib.parse.urlencode(
                {
                    'action': program_list_page_token,
                    'orderBy': '',
                    'oldOrderBy': '',
                    'sortDirection': 'Forward',
                    'keyword': '',
                    'searchBy': 'jobViewCountCurrentTerm',
                    'searchType': '',
                    'initialSearchAction': 'displayViewedJobs',
                    'postings': 'infoForPostings',
                    'page': str(counter),
                    'currentPage': str(counter - 1),
                    'rand': '1'}).encode()

            try:
                time.sleep(counter)
                program_list_content = urllib.request.urlopen(for_my_program_url, selected_program_list_data).read()
                # print(re.findall(r'\=\"\?action=.+?\"\>[\\rnt]+(.+?)\<\/a\>', str(program_list_content)))
            except Exception:
                error_log("Error Found In Acquiring Page " + str(counter))
        else:
            program_list_content = first_page_content

        project_detail_link = re.findall(r'\=\"(\?action=.+?)\"\>', str(program_list_content))
        print(str(len(project_detail_link)) + " for Page: " + str(counter) + " " + str(
            re.findall(r'\=\"\?action=.+?\"\>[\\rnt]+(.+?)\<\/a\>', str(program_list_content))))

        while threading.active_count() > 50:
            time.sleep(2)
            # error_log("Page " + str(counter) + " Waiting")

        attempt_success = False

        def page_complete_call_back(res):
            print("Finished Getting All From Page: " + str(counter))
            resolve(res)

        while attempt_success is False:
            try:
                promises_list = [get_program_detail_content_promise(counter, i, project_detail_link[i]) for i in
                                 range(len(project_detail_link))]
                Promise.all(promises_list).then(page_complete_call_back)
                attempt_success = True
            except Exception as e:
                error_log(str(e) + " Page " + str(counter) + " Failed")
                attempt_success = False
                time.sleep(2)

    return Promise(get_all_page_program_detail)


def log_in():
    # The action/ target from the form
    log_in_url = 'https://cas.uwaterloo.ca/cas/login?service=https://waterlooworks.uwaterloo.ca/waterloo.htm'

    # request password
    # username = input("UserName: ")
    # password = input("Password: ")
    username = "l78zhu"
    password = "#741231lY"
    data = urllib.parse.urlencode(
        {'username': username, 'password': password, '_eventId': 'submit', 'submit': 'LOGIN',
         'lt': 'e1s1'}).encode()

    start_time = time.time()

    print("Log in Into Waterloo Website")
    urllib.request.urlopen(log_in_url)
    urllib.request.urlopen(log_in_url, data)

    # go in to the page of "For My Program"
    for_my_program_page = urllib.request.urlopen(for_my_program_url)
    for_my_program_page_content = for_my_program_page.read()

    token = ""
    token_soup = BeautifulSoup(for_my_program_page_content, "html.parser")
    for link in token_soup.findAll('a'):
        if link.string.strip() == target_section:
            token = re.search("action':'(.+?)'", str(link)).group(1)

    if token is "":
        error_log("Error: " + target_section + " Token Unfound")
        exit()

    print("Getting Target Section Program List")
    # try post to target section
    program_data = urllib.parse.urlencode(
        {'action': token, 'rand': '1'}).encode()
    # get the default first page
    first_page = urllib.request.urlopen(for_my_program_url, program_data)
    first_page_content = first_page.read()

    try:
        program_list_page_token = re.search(
            r"loadPostingTable\(orderBy\, oldOrderBy\, sortDirection\, page[\w\W]+?action[\w\W]+?\'([\w\W]+?)\\\'",
            str(first_page_content)).group(1)
    except Exception:
        error_log("Program Page Switch Token Unfound")
        exit()

    # get the number of pages
    page_count = max(map(int, re.findall(r'null\W+?(\d+)\W+?', str(first_page_content))))

    print("Attempting to Get All Pages")

    all_pages_programs_promise_list = [
        get_all_page_program_detail_content_promise(program_list_page_token, i, first_page_content)
        for i in range(1, page_count + 1)
        ]

    def final_call_back(data):
        print("Organizing data...")
        print("Done! ")

        for each_page in data:
            for each_program in each_page:
                organize_program_info_to_database(each_program)

        print("---- %s seconds ----" % (time.time() - start_time))

    Promise.all(all_pages_programs_promise_list).then(lambda res: final_call_back(res))

    # while True:
    # error_log(threading.active_count())


log_in()
