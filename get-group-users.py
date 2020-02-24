import src.rq as rq
import pprint
import config
import json
import os
import csv
import requests

app_path = os.path.dirname(__file__)
__location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))

groupname = input('Group: ')

file_directory = os.path.expanduser('~/Desktop/api-return/')
filename = groupname+'.csv'


filepath = os.path.join(file_directory, filename)

if not os.path.exists(file_directory):
    os.makedirs(file_directory)

create_file = open(os.path.join(file_directory, filename), 'a')

def pretty(string):
    pp = pprint.PrettyPrinter(indent=4)
    return pp.pprint(string)


def flatten(f_data, d):
    for k, v in d.items():
        if isinstance(v, dict):
            flatten(f_data, v)
        else:
            f_data[k] = v


OKTA_BASE_URL = 'https://[ORGNAME].okta.com/api/v1'
okta_search_group_arguments = {
    'url': OKTA_BASE_URL+'/groups/',
    'headers': {
        'Accept': 'application/json',
        'Content-Type': 'application/json',
        'Authorization': config.okta_api_token,
    },
    'params': {
        'q': groupname,
}
}
okta_user_arguments = {
    'url': OKTA_BASE_URL+'/groups/x/users?limit=200',
    'headers': {
        'Accept': 'application/json',
        'Content-Type': 'application/json',
        'Authorization': config.okta_api_token,
    },
}

def main():
    okta()

def okta():
    def search_okta_group():
        try:
            r = rq.get_url_kwargs(**okta_search_group_arguments)
            data = json.loads(r.content)
            # pretty(data)
            output = [{k: v for k, v in i.items() if k in ['id']} for i in data]
            
            for i in output:
                for k, v in i.items():
                    return v
        except Exception as e:
            print(e)

    okta_group_id = search_okta_group()
    
    okta_user_arguments.update({'url': OKTA_BASE_URL+'/groups/{}/users?limit=200'.format(okta_group_id)})

    def get_group_users():
        try:
            r = rq.get_url_kwargs(**okta_user_arguments)
            data = json.loads(r.content)
            # print(r.links)
            profile = [d['profile'] for d in data] #>>> works
            with open (filepath, 'a') as f:
                headers = ['displayName', 'nickName', 'login', 'email', 'firstName', 'lastName', 'title', 'department', 'manager', 'managementLevel', 'productOrg2', 'productOrg1', 'managerFirstLast', 'employeeNumber', 'state', 'city', 'location', 'hireDate', 'managerUsername', 'isSupervisor', 'payType', 'newHire90', 'userType']
                writer = csv.DictWriter(f, fieldnames=headers, extrasaction='ignore')
                if os.stat(filepath).st_size == 0:
                    writer.writeheader()
                # writer.writeheader()
                writer.writerows(profile)
            # pretty(profile)
            has_next_page = False
            if 'next' in r.links:
                has_next_page = True

            while has_next_page:
                okta_user_arguments.update({'url': '{}'.format(r.links['next']['url'])})
                # print(okta_user_arguments)
                r = rq.get_url_kwargs(**okta_user_arguments)
                data = json.loads(r.content)
                profile = [d['profile'] for d in data]
                # pretty(profile)
                
                with open (filepath, 'a') as f:
                    headers = ['displayName', 'nickName', 'login', 'email', 'firstName', 'lastName', 'title', 'department', 'manager', 'managementLevel', 'productOrg2', 'productOrg1', 'managerFirstLast', 'employeeNumber', 'state', 'city', 'location', 'hireDate', 'managerUsername', 'isSupervisor', 'payType', 'newHire90', 'userType']
                    writer = csv.DictWriter(f, fieldnames=headers, extrasaction='ignore')
                    if os.stat(filepath).st_size == 0:
                        writer.writeheader()
                    # writer.writeheader()
                    writer.writerows(profile)
                if 'next' in r.links:
                    # print(r.links['next'])
                    continue
                else:
                    has_next_page = False
            
                
        except Exception as e:
            print('Exception ', e)

    get_group_users()

if __name__ == "__main__":
    main()