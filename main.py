import requests

class GetDepartureTime:
    # 駅すぱあとのurl.出発：稲毛、目的地：東京
    Url = 'https://roote.ekispert.net/ja/result?arr=%E6%9D%B1%E4%BA%AC&amp;arr_code=22828&amp;connect=true&amp;dep=%E7%A8%B2%E6%AF%9B&amp;dep_code=22197&amp;highway=true&amp;hour&amp;limitedExpress=true&amp;liner=true&amp;local=true&amp;minute&amp;plane=true&amp;shinkansen=true&amp;ship=true&amp;sleep=false&amp;sort=transfer&amp;surcharge=3&amp;type=dep&amp;via1=&amp;via1_code=&amp;via2=&amp;via2_code='

    # 駅すぱあと for WEB にCurlする。クラス変数のUrlを指定
    def curl_to_ekispert(self):
        response = requests.get(self.Url)
        return response

    # curlのレスポンスのtextを"\n"区切りで分割し、リストに変換
    def reform_response(self):
        response = self.curl_to_ekispert()
        responseTexts = response.text.split('\n')
        return responseTexts

    #レスポンスから「経路1」「経路2」..「経路4」をキーワードに発車時刻(hh:mm)を取得し、出力
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

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    getdt = GetDepartureTime()
    outputs = getdt.get_departure_time()
    for output in outputs:
        print(output)
