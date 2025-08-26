#This file is reponsible for making API requests
import logging
import requests
import configparser

# Read from config.ini
config = configparser.ConfigParser()
config.read('config.ini')

API_KEY = config['API']['api_key']
API_ENDPOINT = config['API']['api_endpoint']


def create_alert(row, row_num):
    # Convert values safely to strings and convert to uppercase
    operator = str(row["OPERATOR"]).upper()
    priority = str(row["PRIORITY"]).upper()
    nrql_query = str(row["NRQL_QUERY"]).replace('"', '\\"')


    widget_name= str(row["NAME_OF_WIDGET"])
    title_name= str(row["ALERT_TITLE"])
    condition_name= str(row["CONDITION_NAME"])
    # Build mutation
    mutation = """
mutation {
  alertsNrqlConditionStaticCreate(accountId: %s, policyId: "%s", condition: {
    enabled: false,
    name: "%s",
    description: "%s",
    titleTemplate: "%s",
    nrql: {
      query: "%s",
      dataAccountId: %s
    },
    expiration: null,
    runbookUrl: null
    signal: {
      aggregationWindow: %s,
      fillOption: NONE,
      aggregationDelay: %s,
      aggregationMethod: EVENT_FLOW,
      aggregationTimer: null,
      fillValue: null,
      slideBy: null,
      evaluationDelay: null,
      pollingFrequency: null
    },
    terms: [{
      operator: %s,
      threshold: %s,
      priority: %s,
      thresholdDuration: %s,
      thresholdOccurrences: ALL
    }],
    violationTimeLimitSeconds: %s
  }) {
    id
  }
}
""" % (
        int(row["ACCOUNT_ID"]),
        str(row["POLICY_ID"]),
        str(row["CONDITION_NAME"]),
        str(row["ALERT_DESCRIPTION"]),
        str(row["ALERT_TITLE"]),
        nrql_query,
        int(row["ACCOUNT_ID"]),
        int(row["WINDOW_DURATION"]),
        int(row["DELAY_DURATION"]),
        operator,
        float(row["THRESHOLD"]),
        priority,
        int(row["THRESHOLD_DURATION"]),
        int(row["VIOLATION_TIME_LIMIT"])
    )

    # Send API request
    payload = {"query": mutation}
    headers = {
        "Content-Type": "application/json",
        "API-Key": API_KEY
    }

    response = requests.post(API_ENDPOINT, headers=headers, json=payload)

    if response.status_code != 200:
        raise Exception(f"API HTTP Error: {response.status_code}\n{response.text}")
    print(f"Graph QL request built '{title_name}' for widget '{widget_name}' (Condition: {condition_name})")
    resp_json = response.json()
    if "errors" in resp_json:
        raise Exception(f"API returned errors: {resp_json['errors']}")

    return resp_json["data"]["alertsNrqlConditionStaticCreate"]
