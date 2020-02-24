import src.rq as rq
import pprint
import config
import json
import os
import csv

app_path = os.path.dirname(__file__)
__location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))

file_directory = os.path.expanduser('~/Desktop/api-return/')
filename = 'okta-groups.csv'

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
okta_user_arguments = {
    'url': OKTA_BASE_URL+'/groups',
    'headers': {
        'Accept': 'application/json',
        'Content-Type': 'application/json',
        'Authorization': config.okta_api_token,
    },
    'params': {
        # 'limit': '1000',
        'filter': 'type eq "OKTA_GROUP"'
    }
}

def main():
    okta()

def okta():
    try:
        r = rq.get_url_kwargs(**okta_user_arguments)
        data = json.loads(r.content)
        # pretty(data)
        # output = [{k: v for k, v in i.items() if k in ['id', 'profile']} for i in data]
        profile = [d['profile'] for d in data]
        # output = [{d['name'],d['description']} for d in profile]
        headers = ['name', 'description']
        with open (filepath, 'a') as f:
                writer = csv.DictWriter(f, fieldnames=headers, extrasaction='ignore')
                writer.writeheader()
                writer.writerows(profile)
    except Exception as e:
        print(e)

if __name__ == "__main__":
    main()