import http.client
import json
from xml.etree import ElementTree as ET
import time
import os

ReseveCnt = "1"
preferredSeatLineStart = "E"
preferredSeatNoStart = 7
preferredSeatLineEnd = "I"
preferredSeatNoEnd = 12

# 용아맥
preferredSeatLineStart = "F"
preferredSeatNoStart = 12
preferredSeatLineEnd = "L"
preferredSeatNoEnd = 32

id = "parkjy1917"
mobileNo = "010-9766-2526"
movieCode = ""
playTimeCode = ""
playNum = ""

theaterCode = ""
playYMD = ""
screenCode = ""
playNum = ""
SOCIAL_NO = "900104"
seatInfo = "00102101"
seatPrice = "21000"
seatRating = "01"
ticketType = "01"

# 판교 theaterCode : 0181


def generate_reservation_data(seat_line, seat_no, seat_loc_no):
    conn = http.client.HTTPConnection("ticket.cgv.co.kr")
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
    headers = {
        'accept': "application/json, text/javascript, */*; q=0.01",
        'origin': "http://ticket.cgv.co.kr",
        'x-requested-with': "XMLHttpRequest",
        'user-agent': "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.103 Safari/537.36",
        'content-type': "application/json",
        'cache-control': "no-cache"
        }

    conn.request("POST", "/CGV2011/RIA/CJ000.aspx/CJ_003_4th", payload, headers)

    res = conn.getresponse()
    data = res.read()

    jsonDict = json.loads(data)
    xmlTree = ET.ElementTree(ET.fromstring(jsonDict['d']['data']['DATA']))
    root = xmlTree.getroot()


def check_seat_preferred_line(avail):
    return ord(preferredSeatLineStart) <= ord(avail) <= ord(preferredSeatLineEnd)


def check_seat_preferred_no(avail):
    return preferredSeatNoStart <= int(avail[1:]) <= preferredSeatNoEnd


if __name__ == "__main__":
    got_ticket = False
    count = 0
    while not got_ticket:
        try:
            count += 1
            conn = http.client.HTTPConnection("ticket.cgv.co.kr")
            payload = ["{"
                      "\"REQSITE\":\"x02PG4EcdFrHKluSEQQh4A==\","
                      "\"Language\":\"zqWM417GS6dxQ7CIf65+iA==\","
                      "\"TheaterCd\":\"ayfHrHXNMdZ7VoODaqnlug==\","
                      "\"PlayYMD\":\"kr7ux111zGQ1/pidWK2Gaw==\","
                      "\"ScreenCd\":\"AmhNIZREuaUclhpBeWoJdg==\","
                      "\"PlayNum\":\"hlrIVsrgDYMr7PQdmwAA4w==\"}"]
            # 용아맥 0505 2230
            payload = ["{\"REQSITE\":\"x02PG4EcdFrHKluSEQQh4A==\",\"Language\":\"zqWM417GS6dxQ7CIf65+iA==\",\"TheaterCd\":\"LMP+XuzWskJLFG41YQ7HGA==\",\"PlayYMD\":\"eWoa/YfzV3T4/Qb+nz9p/A==\",\"ScreenCd\":\"puE6q/PuILVnVlbgI8uHnA==\",\"PlayNum\":\"GQ4XBvPgo294+v/kGdDx+Q==\"}"]
            # 판교 imax 0505 1905
            # payload = ["{\"REQSITE\":\"x02PG4EcdFrHKluSEQQh4A==\",\"Language\":\"zqWM417GS6dxQ7CIf65+iA==\",\"TheaterCd\":\"ayfHrHXNMdZ7VoODaqnlug==\",\"PlayYMD\":\"eWoa/YfzV3T4/Qb+nz9p/A==\",\"ScreenCd\":\"am6yhfEj+mm3cbYmAGVHIA==\",\"PlayNum\":\"K69H87N+CcalH4eFao/hAQ==\"}",
            #             "{\"REQSITE\":\"x02PG4EcdFrHKluSEQQh4A==\",\"Language\":\"zqWM417GS6dxQ7CIf65+iA==\",\"TheaterCd\":\"ayfHrHXNMdZ7VoODaqnlug==\",\"PlayYMD\":\"eWoa/YfzV3T4/Qb+nz9p/A==\",\"ScreenCd\":\"am6yhfEj+mm3cbYmAGVHIA==\",\"PlayNum\":\"GQ4XBvPgo294+v/kGdDx+Q==\"}"]
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
            conn.request("POST", "/CGV2011/RIA/CJ000.aspx/CJ_002_PRIME_ZONE_LANGUAGE", payload[count % len(payload)], headers)

            res = conn.getresponse()
            data = res.read()

            jsonDict = json.loads(data)
            xmlTree = ET.ElementTree(ET.fromstring(jsonDict['d']['data']['DATA']))
            root = xmlTree.getroot()
            res = root.find('SEAT_INFO')
            conn_seat = 0
            seat_info = {"seat_loc_no": [], "loc_y_nm": [], "seat_no": []}
            for child in root:
                if child.tag == "SEAT_INFO":
                    seat = child
                    if seat.find("SEAT_STATE").text == "Y":
                        seat_info['seat_loc_no'].append(seat.find("SEAT_LOC_NO").text)
                        seat_info['loc_y_nm'].append(seat.find("LOC_Y_NM").text[:1])
                        seat_info['seat_no'].append(seat.find("SEAT_NO").text)
                        availSeat = seat_info['loc_y_nm'][conn_seat] + str(seat_info['seat_no'][conn_seat][1:])
                        if check_seat_preferred_line(seat_info['loc_y_nm'][conn_seat]) and check_seat_preferred_no(seat_info['seat_no'][conn_seat]):
                            if int(ReseveCnt) >= conn_seat + 1:
                                if conn_seat == 0:
                                    conn_seat += 1
                                    continue
                                else:
                                    if seat_info['loc_y_nm'][conn_seat - 1] == seat_info['loc_y_nm'][conn_seat] and \
                                     int(seat_info['seat_no'][conn_seat]) - int(seat_info['seat_no'][conn_seat - 1]) == 1:
                                        conn_seat += 1
                            if int(ReseveCnt) == conn_seat:
                                print("GOTCHA for " + str(count % 2))
                                a = zip(seat_info["loc_y_nm"], seat_info["seat_no"], seat_info["seat_loc_no"])
                                print(*a)
                                os.system('say "I got a ticket"')
                                os.system('say "I got a ticket"')
                                os.system('say "I got a ticket"')
                                os.system('say "I got a ticket"')
                                os.system('say "I got a ticket"')

                        else:
                            seat_info["seat_loc_no"] = []
                            seat_info["loc_y_nm"] = []
                            seat_info["seat_no"] = []
                            conn_seat = 0
                            continue
                    else:
                        seat_info["seat_loc_no"] = []
                        seat_info["loc_y_nm"] = []
                        seat_info["seat_no"] = []
                        conn_seat = 0
                        continue
            print(".", end='', flush=True)
            time.sleep(1)
        except Exception as e:
            print("Error", e)
            os.system('say "Error"')
            time.sleep(1)
            continue


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