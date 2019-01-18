#!/usr/bin/python

ANSIBLE_METADATA = {
    'metadata_version': '1.1',
    'status': ['preview'],
    'supported_by': 'community'
}

DOCUMENTATION = '''
---
module: config_group
short_description: manage component on a host using ambari rest api
'''

EXAMPLES = '''
- name: add a config group
  host_component:
    username: "ambari"
    url: "https://ambari.metal:8442"
    password: "ambari"
    config_type: "HDFS"
    config_tag: 'datanode storage'
    config_description: 'my beautiful config group'
    hosts:
        - master1.metal
        - master2.metal
    cluster_name: "myCluster"
    validate_certs: no
  register: result
'''

from ansible.module_utils.basic import *
import requests
import base64
from base64 import b64encode

def stringToBase64(s):
    return base64.b64encode(s.encode('utf-8'))

def base64ToString(b):
    return base64.b64decode(b).decode('utf-8')

def get_header(data):
    username = data['username']
    password = data['password']
    headers = {
        "X-Requested-By": "ambari",
        "Content-Type": "application/x-www-form-urlencoded",
        "Authorization": 'Basic %s' % (base64.b64encode( bytes(username + ':' + password, "utf-8"))).decode('utf-8')
    }
    return headers


def group_add(data):
    api_url = data['url']
    api_path = "/api/v1/clusters/" + data['cluster_name'] + "/config_groups"
    url = "{}{}" . format(api_url, api_path)
    hosts = []
    for host in data['hosts']:
        hosts.append({"host_name": host})
    desired_configs = []
    properties = {}
    for prop in data['properties']:
        properties[prop.split('=')[0]] = prop.split('=')[1]
    config = {
        "type": data['config_type'],
        "tag": data['config_tag'],
        "properties": properties
    } 
    content = {
        "ConfigGroup": {
            "cluster_name": data['cluster_name'],
            "group_name": data['group_name'],
            "tag": data['group_tag'],
            "description": data['group_description'],
            "hosts": hosts,
            "desired_configs": [config]
        }
    }
    content = json.dumps(content)
    headers = get_header(data)
    headers["Content-length"] = str(len(content))
    try:
        verify = True 
        if data['validate_certs'] == 'no':
            verify = False
        result = requests.post(url, content, headers=headers, verify= verify, json=content)
        result.raise_for_status()
        if result.status_code in [202]:
            # component does not exist
            return False, True, result
        else:
            # error happened
            return True, False, result
    except requests.exceptions.HTTPError as e: 
        if result.status_code == 409 :
            print('Config group already exist')
            return False, False, result
        else:
            return True, False, result
        # return False, False, {"status": "already exist"}


def main():

 fields = {
	"username": {"required": True, "type": "str"},
	"password": {"required": True, "type": "str" },
    "url": {"required": True, "type": "str" },
    "config_tag": {"required": True, "type": "str" },
    "config_type": {"required": True, "type": "str" },
    "cluster_name": {"required": True, "type": "str" },
    "group_name": {"required": True, "type": "str" },
    "group_description": {"required": True, "type": "str" },
    "group_tag": {"required": True, "type": "str" },
    "properties": {"required": True, "type": "list" },
    "hosts": {"required": True, "type": "list" },
    "validate_certs": {"required": False, "type": "str", "default": "no" },
    "state": {
    	"default": "register", 
    	"choices": ['register'],  
    	"type": 'str' 
    }
  }
  
 module = AnsibleModule(argument_spec=fields)
 is_error, has_changed, result = group_add(module.params)
 if not is_error:
    module.exit_json(changed=has_changed, meta=result, status=result.status_code, error=is_error)
 else:
    module.fail_json(error=is_error, msg="Error adding config group", meta=result)

RETURN = '''
is_error:
    description: If the module has failed
    type: Bool
has_changed:
    description: the status for module idempotent character
result:
    description: the http request result as json dictionnary
'''

if __name__ == '__main__':
    main()