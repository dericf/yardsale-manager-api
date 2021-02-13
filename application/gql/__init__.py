from flask import request

import requests

import json

from config import CONFIG as config

CONFIG = config()


def build_admin_auth_headers(req):
    # api_token = req.headers['Authorization'][1]
    return {
        "X-Hasura-Admin-Secret": CONFIG.GRAPHQL_ADMIN_SECRET
    }


def build_auth_headers(req):
    api_token = req.headers['Authorization'][1]
    return {
        "Authorization": "token %s" % api_token,
        "X-Hasura-User-Id": req.headers['X-Hasura-User-Id'],
        "X-Hasura-Role": req.headers['X-Hasura-Role']
    }


def Query(query, variables=None, as_admin=False):
    '''A Generic GraphQL Query Wrapper
    '''
    query_json = {'query': query}
    if variables:
        query_json['variables'] = variables
    #
    # Build Auth headers
    #
    headers = build_admin_auth_headers(
        request) if as_admin == True else build_auth_headers(request)
    #
    # Send a POST request (fomrated as a GQL Query)
    #
    r = requests.post(url=CONFIG.GRAPHQL_ENDPOINT,
                      json=query_json, headers=headers)

    # Return the resultings data as json (python dictionary)
    try:
        return ((json.loads(r.text))['data'])
    except Exception as e:
        print('\nError with Query: ', r.text)
        return None


def Mutation(mutation, variables=None, as_admin=False):
    '''A Generic GraphQL Mutation Wrapper
    '''
    mutation_json = {'query': mutation}
    if variables:
        mutation_json['variables'] = variables

    headers = build_admin_auth_headers(
        request) if as_admin == True else build_auth_headers(request)

    r = requests.post(url=CONFIG.GRAPHQL_ENDPOINT,
                      json=mutation_json, headers=headers)
    # print('Result from mutation: ', json.loads(r.text))
    # Return the resulting data as json (python dictionary)
    return ((json.loads(r.text)))
