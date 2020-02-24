import src.rq as rq
import pprint
import config
import json
import os
import csv

app_path = os.path.dirname(__file__)
__location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))

groupname = input('Group: ')

prompt_file_location = input ('File Location: ')
file_location = os.path.expanduser(prompt_file_location)

# # filepath = os.path.join(file_directory, filename)
print(file_location)


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
okta_group_user_update_args = {
    'url': OKTA_BASE_URL+'/groups/x/users/x',
    'headers': {
        'Accept': 'application/json',
        'Content-Type': 'application/json',
        'Authorization': config.okta_api_token,
    },
}
okta_user_arguments = {
    'url': OKTA_BASE_URL+'/users/x',
    'headers': {
        'Accept': 'application/json',
        'Content-Type': 'application/json',
        'Authorization': config.okta_api_token,
    }
}

def main():
    okta()

def okta():
    def search_okta_group():
        try:
            r = rq.get_url_kwargs(**okta_search_group_arguments)
            data = json.loads(r.content)
            output = [{k: v for k, v in i.items() if k in ['id']} for i in data]
            
            for i in output:
                for k, v in i.items():
                    return v
        except Exception as e:
            print(e)

    okta_group_id = search_okta_group()
    userids = []

    def get_okta_user_ids():
        try:
            with open(file_location) as f:
                read_csv = csv.DictReader(f)
                for row in read_csv:
                    okta_user_arguments.update({'url': OKTA_BASE_URL+'/users/{}'.format(row['username'])})
                    r = rq.get_url_kwargs(**okta_user_arguments)  
                    data = json.loads(r.content)
                    userids.append(data['id'])


        except Exception as e:
            print(e)

    get_okta_user_ids()
    print(userids)

    def push_okta_user_to_group():
        try:
            for i in userids:
                okta_group_user_update_args.update({'url': OKTA_BASE_URL+'/groups/{}/users/{}'.format(okta_group_id, i)})
                r = rq.put_url_kwargs(**okta_group_user_update_args)
        except Exception as e:
            print(e)

    push_okta_user_to_group()
    





if __name__ == "__main__":
    main()