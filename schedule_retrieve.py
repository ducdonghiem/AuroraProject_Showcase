import requests
from bs4 import BeautifulSoup
from dotenv import load_dotenv
import os


def schedule_retrieve(term, course_list):
    schedule_list = []
    weirdCourses = []
    load_dotenv()  # Load environment variables from .env file
    id = os.getenv("ID")
    pin = os.getenv("PIN")
    sessid = login(id, pin)
    for course in course_list:
        subj, crse = list(course.items())[0]
        cookies = {
            'TESTID': 'set',
            'SESSID': sessid,
            'BIGipServer~INB_SSB_Flex~Banner_Self_Service_BANPROD_pool': '336723978.64288.0000',
            '_gcl_au': '1.1.1976295298.1708504805',
            '_tt_enable_cookie': '1',
            '_ttp': 'M8LOJTJwcr-V4u31oIoPweCS_g9',
            '_fbp': 'fb.1.1708504805446.430921143',
            'accessibility': 'false',
            '_gid': 'GA1.2.1525560649.1708677043',
            'TS01c6c21c': '010e8404412caae9eed6af3ae840c1b3ca974cd44ef167ec5ea43689175a83b23a2f4c88e8930d02daabe7b9a56e969489fee24649',
            'jcoPageCount': '21',
            '_ga': 'GA1.2.1269208878.1708504805',
            '_ga_5KL2MD48DQ': 'GS1.1.1708713725.3.1.1708713895.60.0.0',
        }
        headers = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
            'Accept-Language': 'en-US,en;q=0.9,vi;q=0.8',
            'Cache-Control': 'max-age=0',
            'Connection': 'keep-alive',
            'Content-Type': 'application/x-www-form-urlencoded',
            'Origin': 'https://aurora.umanitoba.ca',
            'Referer': 'https://aurora.umanitoba.ca/ssb/bwskfcls.P_GetCrse',
            'Sec-Fetch-Dest': 'document',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-Site': 'same-origin',
            'Sec-Fetch-User': '?1',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36 Edg/121.0.0.0',
            'sec-ch-ua': '"Not A(Brand";v="99", "Microsoft Edge";v="121", "Chromium";v="121"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
        }
        data = {
            'term_in': term,
            'sel_subj': [
                'dummy',
                subj,
            ],
            'SEL_CRSE': crse,
            'SEL_TITLE': '',
            'BEGIN_HH': '0',
            'BEGIN_MI': '0',
            'BEGIN_AP': 'a',
            'SEL_DAY': 'dummy',
            'SEL_PTRM': 'dummy',
            'END_HH': '0',
            'END_MI': '0',
            'END_AP': 'a',
            'SEL_CAMP': 'dummy',
            'SEL_SCHD': 'dummy',
            'SEL_SESS': 'dummy',
            'SEL_INSTR': [
                'dummy',
                '%',
            ],
            'SEL_ATTR': [
                'dummy',
                '%',
            ],
            'SEL_LEVL': [
                'dummy',
                '%',
            ],
            'SEL_INSM': 'dummy',
            'sel_dunt_code': '',
            'sel_dunt_unit': '',
            'call_value_in': '',
            'rsts': 'dummy',
            'crn': 'dummy',
            'path': '1',
            'SUB_BTN': 'View Sections',
        }

        s = requests.Session()
        response = s.post('https://aurora.umanitoba.ca/ssb/bwskfcls.P_GetCrse', cookies=cookies, headers=headers, data=data)
        sessid = response.cookies.get('SESSID')
        scheduleA = {} 
        scheduleB = {}
        scheduleC = {}
        soup = BeautifulSoup(response.text, 'html.parser')
        if soup.title.text == "Site maintenance":
            return ("Maintenance", weirdCourses)
        table = soup.find(class_='datadisplaytable', recursive=True)
        if table:
            rows = table.find_all('tr')
            for row in rows:
                columns = row.find_all('td', recursive=False)
                if len(columns) >= 10:
                    if columns[2].text.isspace():
                        day = columns[8].text
                        time = columns[9].text
                        scheduleC[course] = [time, day, crn, enrolled, wailist, instructor, location, status]  # the second time slot of course with two time slots, ex: ENG1450
                        continue
                    time = columns[9].text
                    day = columns[8].text
                    if time == "TBA" or day == "TBA":        
                        continue    
                    # Find the <span> inside the <label>
                    span = columns[0].find('label').find('span') if columns[0].find('label') else None
                    if span and span.text == "add to worksheet":
                        status = "Open"
                    elif columns[0].find('abbr', title='Closed'):
                        status = "Closed"
                    elif columns[0].find('abbr', title= 'Not available for registration'):
                        status = "Not available for registration"
                    else:
                        status = "Check it yourself"
                    course = columns[2].text + columns[3].text + columns[4].text
                    enrolled = columns[11].text + "/" + columns[10].text
                    wailist =  columns[14].text + "/" + columns[13].text
                    instructor = columns[16].text
                    location = columns[18 ].text
                    crn = "CRN=" + columns[1].text
                    if columns[4].text[0] == 'A':
                        scheduleA[course] = [time, day, crn, enrolled, wailist, instructor, location, status]
                    elif columns[4].text[0] == 'B':
                        scheduleB[course] = [time, day, crn, enrolled, wailist, instructor, location, status]
            if len(scheduleA) != 0:
                schedule_list.append(scheduleA)
            if len(scheduleB) != 0:
                schedule_list.append(scheduleB)  # separate A and B sections into different dicts to choose only one class from each  
            if len(scheduleC) != 0:
                weirdCourses.append(course[0:-3])
                schedule_list.append(scheduleC)
        else:
            return (subj+crse, weirdCourses)  
    print(schedule_list)
    return (schedule_list, weirdCourses)  

def login(id, pin):
    cookies = {
        'TESTID': 'set',
        'BIGipServer~INB_SSB_Flex~Banner_Self_Service_BANPROD_pool': '336723978.64288.0000',
        '_gcl_au': '1.1.1976295298.1708504805',
        '_tt_enable_cookie': '1',
        '_ttp': 'M8LOJTJwcr-V4u31oIoPweCS_g9',
        '_fbp': 'fb.1.1708504805446.430921143',
        'accessibility': 'false',
        'TS01c6c21c': '010e840441326cab8ab4473cb05907b9c0dee7fa50f31afdc15e8681820abb4874da67c8d79fb2a6bcfcfb5a5faad1a464e07b5cce',
        '_gid': 'GA1.2.1525560649.1708677043',
        'jcoPageCount': '20',
        '_ga': 'GA1.1.1269208878.1708504805',
        '_ga_5KL2MD48DQ': 'GS1.1.1708677042.2.1.1708677161.5.0.0',
    }
    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'Accept-Language': 'en-US,en;q=0.9,vi;q=0.8',
        'Cache-Control': 'max-age=0',
        'Connection': 'keep-alive',
        'Content-Type': 'application/x-www-form-urlencoded',
        'Origin': 'https://aurora.umanitoba.ca',
        'Referer': 'https://aurora.umanitoba.ca/ssb/twbkwbis.P_WWWLogin',
        'Sec-Fetch-Dest': 'document',
        'Sec-Fetch-Mode': 'navigate',
        'Sec-Fetch-Site': 'same-origin',
        'Sec-Fetch-User': '?1',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36 Edg/121.0.0.0',
        'sec-ch-ua': '"Not A(Brand";v="99", "Microsoft Edge";v="121", "Chromium";v="121"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
    }
    data = {
        'sid': id,
        'PIN': pin,
    }
    s = requests.Session() 
    response = s.post('https://aurora.umanitoba.ca/ssb/twbkwbis.P_ValLogin', cookies=cookies, headers=headers, data=data)
    sessid = response.cookies.get('SESSID') 
    return sessid
    
