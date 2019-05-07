import http.client
import json
from xml.etree import ElementTree as ET
import time
import os

preferredSeatLineStart = "F"
preferredSeatNoStart = 7
preferredSeatLineEnd = "I"
preferredSeatNoEnd = 12

id = "parkjy1917"
mobileNo = "010-9766-2526"
movieCode = ""
playTimeCode = ""
playNum = ""

theaterCode = ""
playYMD = ""
screenCode = ""
playNum = ""
ReseveCnt = "1"
SOCIAL_NO = "900104"
seatInfo = "00102101"
seatPrice = "21000"
seatRating = "01"
ticketType = "01"

# 판교 theaterCode : 0181

def generate_reservation_data(seatL, seatN):
    # payload = "{" \
    #           "\"LOC_Y_NM\":\"" + seatL + "\"," \
    #           "\"Language\":\"zqWM417GS6dxQ7CIf65+iA==\"," \
    #           "\"TheaterCd\":\"" + theaterCode + "\"," \
    #           "\"PlayYMD\":\"" + playYMD + "\"," \
    #           "\"ScreenCd\":\"puE6q/PuILVnVlbgI8uHnA==\"," \
    #           "\"PlayNum\":\"GQ4XBvPgo294+v/kGdDx+Q==\"," \
    #           "\"PlayYMD\":\"" + playYMD + "\"," \
    #           "\"ReseveCnt\":\"" + ReseveCnt + "\"," \
    #           "\"SEAT_NM\":\"" + seatN + "\"," \
    #           "\"SOCIAL_NO\":\"" + SOCIAL_NO + "\"," \
    #           "\"ScreenCd\":\"" + screenCode + "\"," \
    #           "\"SeatInfo\":\"" + seatInfo + "\"," \
    #           "\"SeatPriceInfo\":\"" + seatPrice + "\"," \
    #           "\"SeatRatingInfo\":\"" + seatRating + "\"," \
    #           "\"TicketTypeInfo\":\"" + ticketType + "\"," \
    #           "}"
    payload = "{" \
              "\"REQSITE\":\"x02PG4EcdFrHKluSEQQh4A==\"," \
              "\"TheaterCd\":\"ayfHrHXNMdZ7VoODaqnlug==\"," \
              "\"PlayYMD\":\"kr7ux111zGQ1/pidWK2Gaw==\"," \
              "\"ScreenCd\":\"AmhNIZREuaUclhpBeWoJdg==\"," \
              "\"PlayNum\":\"hlrIVsrgDYMr7PQdmwAA4w==\"," \
              "\"ReseveCnt\":\"eUHdeAgG0OAi96HPh0I1jQ==\"," \
              "\"SeatInfo\":\"AQb1Ev1VgWCEK/psPuCJULzRpHwcVB4rKvEAN45eros=\"," \
              "\"SeatRatingInfo\":\"JY3R6evneBB0ubbtS69Bxg==\"," \
              "\"TicketTypeInfo\":\"JKahvX/IzoOspxVsincD7w==\"," \
              "\"SeatPriceInfo\":\"I0svAL3VT5du2F75enhqiw==\"," \
              "\"LOC_Y_NM\":\"3yVaocx2Foot4wP7qlkaAQ==\"," \
              "\"SEAT_NM\":\"1sgD+d0CJdh8uNTABI9w1Q==\"," \
              "\"MEMBER_ID\":\"DhwdZi7eU7NZ7Tx5V/fqYQ==\"," \
              "\"SOCIAL_NO\":\"CG/Wetx/wrujVmtVQma7FQ==\"," \
              "\"MOBILE_NO\":\"fgmM0LXYb1/JmBdnVTFkNF3CNFM0FOcMCf+7KCV3ncw=\"," \
              "\"MOVIE_CD\":\"loLhfGqBSIvZFUdh9agR8w==\"," \
              "\"PLAY_TIME_CD\":\"rx1JL+MSPjub5lRmoqM/FA==\"" \
              "}"


def check_seat_preferred_line(avail):
    return ord(preferredSeatLineStart) <= ord(avail) <= ord(preferredSeatLineEnd)


def check_seat_preferred_no(avail):
    return preferredSeatNoStart <= int(avail.text[1:]) <= preferredSeatNoEnd


if __name__ == "__main__":
    got_ticket = False
    while not got_ticket:
        conn = http.client.HTTPConnection("ticket.cgv.co.kr")
        payload = "{" \
                  "\"REQSITE\":\"x02PG4EcdFrHKluSEQQh4A==\"," \
                  "\"Language\":\"zqWM417GS6dxQ7CIf65+iA==\"," \
                  "\"TheaterCd\":\"ayfHrHXNMdZ7VoODaqnlug==\"," \
                  "\"PlayYMD\":\"kr7ux111zGQ1/pidWK2Gaw==\"," \
                  "\"ScreenCd\":\"AmhNIZREuaUclhpBeWoJdg==\"," \
                  "\"PlayNum\":\"hlrIVsrgDYMr7PQdmwAA4w==\"}"
        #
        # payload = "{" \
        #           "\"REQSITE\":\"x02PG4EcdFrHKluSEQQh4A==\"," \
        #           "\"Language\":\"zqWM417GS6dxQ7CIf65+iA==\"," \
        #           "\"TheaterCd\":\"" + theaterCode + "\"," \
        #           "\"PlayYMD\":\"" + playYMD + "\"," \
        #           "\"ScreenCd\":\"" + screenCode + "\"," \
        #           "\"PlayNum\":\"" + playNum + "\"" \
        #           "}"
        headers = {
            'accept': "application/json, text/javascript, */*; q=0.01",
            'origin': "http://ticket.cgv.co.kr",
            'x-requested-with': "XMLHttpRequest",
            'user-agent': "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.103 Safari/537.36",
            'content-type': "application/json",
            'cache-control': "no-cache"
            }
        conn.request("POST", "/CGV2011/RIA/CJ000.aspx/CJ_002_PRIME_ZONE_LANGUAGE", payload, headers)

        res = conn.getresponse()
        data = res.read()

        jsonDict = json.loads(data)
        xmlTree = ET.ElementTree(ET.fromstring(jsonDict['d']['data']['DATA']))
        root = xmlTree.getroot()
        res = root.find('SEAT_INFO')
        seat_info_dict = {'loc_y_nm': }
        for child in root:
            if child.tag == "SEAT_INFO":
                seat = child
                if seat.find("SEAT_STATE").text == "Y":
                    availSeatLine = seat.find("LOC_Y_NM").text[:1]
                    availSeatNo = seat.find("SEAT_NO")
                    availSeat = availSeatLine + str(availSeatNo.text[1:])
                    if check_seat_preferred_line(availSeatLine) and check_seat_preferred_no(availSeatNo):
                        print("GOTCHA : " + availSeat)
                        os.system('say "I got a ticket"')
                        os.system('say "I got a ticket"')
                        os.system('say "I got a ticket"')
                        os.system('say "I got a ticket"')
                        os.system('say "I got a ticket"')
                    else:
                        continue
        print(".", end='')
        time.sleep(3)


"""

LOC_Y_NM: "A"
MEMBER_ID: "parkjy1917"
MOBILE_NO: "r7U7j0uw7P3/fDQ4iEE1TA=="
MOVIE_CD: "20019370"
PLAY_TIME_CD: "26"
PlayNum: "4"
PlayYMD: "20190503"
ReseveCnt: 1
SEAT_NM: "019"
SOCIAL_NO: "900104"
ScreenCd: "018"
SeatInfo: "00102101"
SeatPriceInfo: "21000"
SeatRatingInfo: "01"
TheaterCd: "0013"
TicketTypeInfo: "01"
"""