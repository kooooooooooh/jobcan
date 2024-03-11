from googleapiclient.discovery import build
import time
import datetime


#カレンダー書き込みの際に、同じ予定があるかチェックする関数
def check_duplicate_events(calendar_id, credentials, googlestart_date, googleend_date, shift_date, endtime):
    service = build('calendar', 'v3', credentials=credentials)
    events = service.events()

    # カレンダーから同じ日時のイベントを取得
    events_result = events.list(calendarId=calendar_id, timeMin=googlestart_date, timeMax=googleend_date).execute()

    year, month, day = map(int, shift_date.split('-'))

    # 数字が10以下の場合には先頭に0を追加する
    if month < 10:
        month_str = f"0{month}"
    else:
        month_str = str(month)

    if day < 10:
        day_str = f"0{day}"
    else:
        day_str = str(day)

    formatted_date = f"{year}-{month_str}-{day_str}"
    formatted_date = formatted_date + "T" + endtime

    if not events_result:
        return False
    for event in events_result['items']:
        start = event['start'].get('dateTime', event['start'].get('date'))
        print("start", start)
        print("formatteddate", formatted_date)
        if start == formatted_date:
            print("同じ予定があるので中止")
            return True
    return False



# Googleカレンダーにイベントを追加する関数
def add_event_to_calendar(calendar_id, credentials, event_data):
    service = build('calendar', 'v3', credentials=credentials)
    events = service.events()
    event_id = str(int(time.time()))

    event = {
        'summary': event_data['summary'],
        'description': event_data.get('description', ''),
        'start': {
            'dateTime': event_data['start']['dateTime'],  # 修正: dateTime を使用
            'timeZone': 'Asia/Tokyo',  # タイムゾーンを指定
        },
        'end': {
            'dateTime': event_data['end']['dateTime'],  # 修正: dateTime を使用
            'timeZone': 'Asia/Tokyo',
        },
    }
    try:
        event = events.insert(calendarId=calendar_id, body=event).execute()
        print(f"Event created: {event.get('htmlLink')}")
    except Exception as e:
        print(f"Error inserting event: {e}")
        print(f"API response: {e.content}")

#ジョブカンから引っ張って来る期間の計算をする。
def calc_date(start_date, end_date):
    now_date = datetime.datetime.today()
    year = now_date.year
    month = now_date.month

    for i in range(2):
        start_date.append(str(year) + "-" + str(month) + "-11")
        if month == 12:
            year += 1
            month = 1
            end_date.append(str(year) + "-1-10")
        else:
            month += 1
            end_date.append(str(year) + "-" + str(month) + "-10")
        print(start_date[i], end_date[i])