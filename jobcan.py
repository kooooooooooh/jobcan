import requests
from bs4 import BeautifulSoup

# ジョブカンにログインしてセッションを確立する関数
def login_to_jobcan(companyname, username, password):
    login_url = "https://ssl.jobcan.jp/login/pc-employee-global?lang_code=ja"
    

    session = requests.Session()
    response = session.post(
        url = login_url,
        data = {
            "client_id" : companyname,
            "email" : username,
            "password" : password,
        }
    )

    # ログイン
    if "打刻" in response.text:
        print("ログインに成功しました。")
        return session
    else:
        print("ログインに失敗しました。")






# ジョブカンからシフト情報を取得する関数
def get_shift_info(session, start, end, shift_date, shift_time):

    start_year, start_month, start_date = map(int, start.split("-"))
    end_year, end_month, end_date = map(int, end.split("-"))
    shift_url = f"https://ssl.jobcan.jp/employee/shift-schedule/?search_type=month&year={end_year}&month={end_month}&from%5By%5D={start_year}&from%5Bm%5D={start_date}&from%5Bd%5D={start_date}&to%5By%5D={start_year}&to%5Bm%5D={start_month}&to%5Bd%5D={end_date}"


    # シフト情報ページにアクセス
    response = session.get(shift_url)
    soup = BeautifulSoup(response.text, 'html.parser')

    # シフト情報を抽出


    # 日付を取得して配列に追加
    date_td = soup.find('td', class_='align-middle')

    while date_td:
        date_text = date_td.get_text(strip=True)  # 12/27(水)
        date = date_text.split('(')[0]  # 日付部分のみ取得
        date_month, date_date = map(int, date.split("/"))

        # 開始時間と終了時間を取得して配列に追加
        start_time_td = date_td.find_next_sibling('td', class_='align-middle')
        start_time_td = start_time_td.find_next_sibling('td', class_='align-middle')
        end_time_td = start_time_td.find_next_sibling('td', class_='align-middle')
        start_time = start_time_td.get_text(strip=True)  # 09:00
        end_time = end_time_td.get_text(strip=True)  # 12:00

        if start_time != "-":
            if start_month == 12 and date_month == 1:
                date_calender = '-'.join([str(start_year + 1), str(date_month), str(date_date)])
            else:
                date_calender = '-'.join([str(start_year), str(date_month), str(date_date)])
            time_calender = '-'.join([str(start_time), str(end_time)])
            shift_date.append(date_calender)
            shift_time.append(time_calender)

        if end_date == date_date:
            break
        
        # 次の日付を表すtd要素を取得
        tr_parent = date_td.parent  # 親のtr要素を取得
        if tr_parent.find_next_sibling('tr').find('td', class_='align-middle') is None:
            break
        next_date_td = tr_parent.find_next_sibling('tr').find('td', class_='align-middle')
        # 次のtr要素を取得してからtd要素を取得

        date_td = next_date_td