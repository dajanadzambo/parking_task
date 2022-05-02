import json
import datetime
import re


def get_receipt(plate, date, card_number):
    """Method for getting the receipt from logs

    Args:
        plate(string): License plate of the vehicle
        date(string): Date of receipt
        card_number(string): Last 4 digits of the card number

    Returns:
        (string): Returns a receipt if one exists. Returns a message
        when an error occurs,
    """

    # checks if the parameters have a valid format
    if plate == "" or date == "" or card_number == "":
        return "Entered data is incomplete!"

    pattern = re.compile("^[A-Z0-9 ]*$")
    check = pattern.match(plate)

    if check is None:
        return "Plate format is wrong!"

    pattern = re.compile("^(0[1-9]|[12][0-9]|3[01])[-](0[1-9]|1[012])[-](19|20)\d\d$")
    check = pattern.match(date)

    if check is None:
        return "Date format is wrong!"

    pattern = re.compile("^[0-9]{4}$")
    check = pattern.match(card_number)

    if check is None:
        return "Card number format is wrong!"

    # turning json line object into json
    data = []

    with open('logs.json') as f:
        for line in f:
            data.append(json.loads(line))

    jsonstring = json.dumps(data)
    jsonfile = open("data.json", "w")
    jsonfile.write(jsonstring)
    jsonfile.close()

    # fetching json from file
    with open('data.json', 'r') as h:
        payload = json.load(h)

    # checking if receipt exists
    for index in range(len(payload)):
        try:
            card_number_from_payload = (payload[index][1]["payment_payload"]["extra"]["card_number"]).replace(' ', '')
            last_4_digits = card_number_from_payload[-5:-1]
            time_from_payload = datetime.datetime.fromtimestamp(payload[index][1]["timestamp"]).strftime('%d-%m-%Y')
            plate_from_payload = payload[index][1]["om_payload"]["id"].replace(' ', '')
            receipt = payload[index][1]["receipt"]
            if time_from_payload == date and last_4_digits == card_number and plate_from_payload == plate:
                return receipt
        except KeyError:
            if index == (len(payload)-1):
                return "There is no receipt for entered data!"
            continue
