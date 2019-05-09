import http.client
import json
from xml.etree import ElementTree
import time
import os

os_name = os.name

# 구하는 인원 수
num_of_people = "2"

# 대충 보면 알것같고..
preferredSeatLineStart = "A"
preferredSeatNoStart = 12
preferredSeatLineEnd = "L"
preferredSeatNoEnd = 32

# 한자리만 찾아도 일단 알려주길 원한다면 True
also_notify_just_one = False


payloads_with_data = [
    ["{\"REQSITE\":\"x02PG4EcdFrHKluSEQQh4A==\",\"Language\":\"zqWM417GS6dxQ7CIf65+iA==\",\"TheaterCd\":\"LMP+XuzWskJLFG41YQ7HGA==\",\"PlayYMD\":\"JFQ+RQXJ8Uin2E/NDXx6+Q==\",\"ScreenCd\":\"puE6q/PuILVnVlbgI8uHnA==\",\"PlayNum\":\"hlrIVsrgDYMr7PQdmwAA4w==\"}", "용아맥 0512 1415"],
    ["{\"REQSITE\":\"x02PG4EcdFrHKluSEQQh4A==\",\"Language\":\"zqWM417GS6dxQ7CIf65+iA==\",\"TheaterCd\":\"LMP+XuzWskJLFG41YQ7HGA==\",\"PlayYMD\":\"JFQ+RQXJ8Uin2E/NDXx6+Q==\",\"ScreenCd\":\"puE6q/PuILVnVlbgI8uHnA==\",\"PlayNum\":\"K69H87N+CcalH4eFao/hAQ==\"}", "용아맥 0512 1745"],
    ["{\"REQSITE\":\"x02PG4EcdFrHKluSEQQh4A==\",\"Language\":\"zqWM417GS6dxQ7CIf65+iA==\",\"TheaterCd\":\"LMP+XuzWskJLFG41YQ7HGA==\",\"PlayYMD\":\"JFQ+RQXJ8Uin2E/NDXx6+Q==\",\"ScreenCd\":\"puE6q/PuILVnVlbgI8uHnA==\",\"PlayNum\":\"GQ4XBvPgo294+v/kGdDx+Q==\"}", "용아맥 0512 2115"]
]


def notify(title, subtitle, message):
    if os_name == "Darwin" or "posix":
        os.system('osascript -e \'display notification "' + message + '" with title "' + title + '" subtitle "' + subtitle + '"\'')
        os.system('say "I got a ticket"')


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

            payload = []
            data_info = []

            for pd in payloads_with_data:
                payload.append(pd[0])
                data_info.append(pd[1])

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
            xmlTree = ElementTree.ElementTree(ElementTree.fromstring(jsonDict['d']['data']['DATA']))
            root = xmlTree.getroot()
            res = root.find('SEAT_INFO')
            seat_info = {"seat_loc_no": "", "loc_y_nm": "", "seat_no": ""}
            found_ticket = False
            preferredSeat = []
            availSeat = []
            if count == 1:
                for info in data_info:
                    print(*info)
                print("검색대상 좌석 : " + preferredSeatLineStart + str(preferredSeatNoStart) + " - " + preferredSeatLineEnd + str(preferredSeatNoEnd))
            for child in root:
                if child.tag == "SEAT_INFO":
                    # 예매가 안된 자리 체크
                    if child.find("SEAT_STATE").text == "Y":
                        # seat_info에 해당 자리 정보 저장
                        seat_info['seat_loc_no'] = child.find("SEAT_LOC_NO").text
                        seat_info['loc_y_nm'] = child.find("LOC_Y_NM").text[:1]
                        seat_info['seat_no'] = child.find("SEAT_NO").text
                        availSeat_tmp = seat_info['loc_y_nm'] + str(seat_info['seat_no'][1:])
                        # preferredSeat 검사
                        if check_seat_preferred_line(seat_info['loc_y_nm']) and check_seat_preferred_no(seat_info['seat_no']):
                            # preferredSeat에 추가
                            preferredSeat.append(seat_info.copy())
                            availSeat.append(availSeat_tmp)
                            # 하나만 발견해도 노티 달라고 해놨다면
                            if also_notify_just_one:
                                # 일단 하나 노티
                                print("Found One Ticket for " + data_info[count % len(payload)] + ", " + availSeat[-1])
                                notify(title="CGV", subtitle="1 Ticket", message=data_info[count % len(payload)])
                            # 아직 원하는 자릿수만큼 preferredSeat를 찾지 못했다면
                            if len(preferredSeat) <= int(num_of_people) and len(preferredSeat) != 1:
                                # 연석인지 체크해서 아니면 preferredSeat 후보에서 삭제하고 다시 loop
                                if not preferredSeat[len(preferredSeat) - 2]['loc_y_nm'] == seat_info['loc_y_nm'] and \
                                 not int(seat_info['seat_no']) - int(preferredSeat[len(preferredSeat) - 2]['seat_no']) == 1:
                                    preferredSeat = []
                                    availSeat = []
                                    found_ticket = False
                                    continue
                        if int(num_of_people) == len(preferredSeat):
                            print("Found Whole Ticket for " + data_info[count % len(payload)] + " ", end='', flush=True)
                            print(*availSeat)
                            notify(title="CGV", subtitle=num_of_people + " Tickets", message=str(data_info[count % len(payload)]))
                            found_ticket = True
                    else:
                        preferredSeat = []
                        availSeat = []
                        continue
            print(".", end='', flush=True)
            time.sleep(2 / len(payload))
        except Exception as e:
            print("Error", e)
            os.system('say "Error"')
            time.sleep(1)
            continue
