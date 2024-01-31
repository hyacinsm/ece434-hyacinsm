#!/usr/bin/env python3
#
#   Author: Sean Hyacinthe
#   Date: 2/04/24
#
#   Description: Reads temperature on 3 MAX31820 sensors using 1 wire protocol
#
#   Setup:  Use .dts file to conigure pin P9.14 as a 1 wire protocol pin
#
#
#   Wiring: P9.14 is configured as a 1 wire pin using device treee service files 


import time
import os.path
import sys

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]

# The ID and range of a sample spreadsheet.
SAMPLE_SPREADSHEET_ID = "1l4uoYMaoVd4WPqNaymDagg596bNthIYDoul7f0Gw5Cw"
SAMPLE_RANGE_NAME = "A2"

HWMON_0 = '/sys/class/hwmon/hwmon0'
HWMON_1 = '/sys/class/hwmon/hwmon1'
HWMON_2 = '/sys/class/hwmon/hwmon2'

TEMP_READING = '/temp1_input'
CELSIUS_MULTIPLIER = 1/1000
SAMPLE_RATE = 60

hw0_fd = open(HWMON_0 + TEMP_READING, "r")
hw1_fd = open(HWMON_1 + TEMP_READING, "r")
hw2_fd = open(HWMON_2 + TEMP_READING, "r")

creds = None
if os.path.exists("token.json"):
    creds = Credentials.from_authorized_user_file("token.json", SCOPES)
    # If there are no (valid) credentials available, let the user log in.
if not creds or not creds.valid:
    if creds and creds.expired and creds.refresh_token:
        creds.refresh(Request())
    else:
        flow = InstalledAppFlow.from_client_secrets_file(
                "credentials.json", SCOPES
            )
        creds = flow.run_console()
        # Save the credentials for the next run
    with open("token.json", "w") as token:
        token.write(creds.to_json())
service = build("sheets", "v4", credentials=creds)

sheet = service.spreadsheets()


while True:
    try:
        hw0_fd.seek(0)
        hw1_fd.seek(0)
        hw2_fd.seek(0)

        hw0_val = round(float(hw0_fd.read().strip()) * CELSIUS_MULTIPLIER, 2)
        hw1_val = round(float(hw1_fd.read().strip()) * CELSIUS_MULTIPLIER, 2)
        hw2_val = round(float(hw2_fd.read().strip()) * CELSIUS_MULTIPLIER, 2)

        data = [hw0_val, hw1_val, hw2_val]
        print(data)

        values = [[time.time()/60/60/24 + 25569 - 4/24,
                   data[0], data[1], data[2]]]
        body = {'values': values}
        result = sheet.values().append(spreadsheetId=SAMPLE_SPREADSHEET_ID,
                                       range=SAMPLE_RANGE_NAME,
                                       valueInputOption='USER_ENTERED',
                                       body=body
                                       ).execute()
        print(result)

    except IOError as e:
        print(f"Error reading or seeking in file: {e}")

    time.sleep(SAMPLE_RATE)
