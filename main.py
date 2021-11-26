import requests
import datetime

class GetDepartureTime:
    def __init__(self, urlcode, code):
        # 駅すぱあとのurl。目的地をurlcode、codeで指定。出発は稲毛
        self.Url = 'https://roote.ekispert.net/ja/result?arr=' + urlcode + '&amp;arr_code=' + code + '&amp;connect=true&amp;dep=%E7%A8%B2%E6%AF%9B&amp;dep_code=22197&amp;highway=true&amp;hour&amp;limitedExpress=true&amp;liner=true&amp;local=true&amp;minute&amp;plane=true&amp;shinkansen=true&amp;ship=true&amp;sleep=false&amp;sort=transfer&amp;surcharge=3&amp;type=dep&amp;via1=&amp;via1_code=&amp;via2=&amp;via2_code='

    # 駅すぱあと for WEB にCurlする。クラス変数のUrlを指定
    def curl_to_ekispert(self):
        response = requests.get(self.Url)
        return response

    # curlのレスポンスのtextを"\n"区切りで分割し、リストに変換
    def reform_response(self):
        response = self.curl_to_ekispert()
        responseTexts = response.text.split('\n')
        return responseTexts

    # レスポンスから「経路1」「経路2」..「経路4」をキーワードに発車時刻(hh:mm)を取得し、出力
    def get_departure_time(self):
        responseTexts = self.reform_response()
        departureTimes = []
        indexTargets = {}

        for index, responseText in enumerate(responseTexts):
            for i in range(4):
                if '経路' + str(i + 1) in responseText:
                    indexTargets[i + 1] = index

        for indexTarget in indexTargets.values():
            departureTimes.append(responseTexts[indexTarget + 3][:5])

        return departureTimes

    def cal_diff_from_now(self, departureTime):
        departure_h = int(departureTime.split(":")[0])
        departure_m = int(departureTime.split(":")[1])

        dt_now = datetime.datetime.now()

        if departure_h < dt_now.hour:
            departure_time = datetime.datetime(dt_now.year, dt_now.month, dt_now.day + 1, departure_h, departure_m)
        else:
            departure_time = datetime.datetime(dt_now.year, dt_now.month, dt_now.day, departure_h, departure_m)

        diff = departure_time - dt_now
        if diff.days < 0:
            return "1分以内の"
        else:
            diff_m = str(diff.seconds / 60).split('.')[0]
            # diff_s = str(diff.seconds - int(diff_m) * 60)

            return str(int(diff_m) + 1) + "分後の"


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    # getdt = GetDepartureTime('%E6%9D%B1%E4%BA%AC', '22828')
    getdt = GetDepartureTime('%E5%8D%83%E8%91%89', '22361')
    outputs = getdt.get_departure_time()
    for output in outputs:
        diff = getdt.cal_diff_from_now(output)
        print(diff + output)
