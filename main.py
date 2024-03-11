from google.oauth2 import service_account

import jobcan
import google_calendar
import send_mail
import key

# メインの処理
if __name__ == "__main__":
    shift_date = []
    shift_time = []

    # ジョブカンへログイン
    jobcan_session = jobcan.login_to_jobcan(key.jobcan_companyname, key.jobcan_username, key.jobcan_password)
    if jobcan_session:
        start_date = []
        end_date = []
        google_calendar.calc_date(start_date, end_date)
        for i in range(2):
            jobcan.get_shift_info(jobcan_session, start_date[i], end_date[i], shift_date, shift_time)
            size = len(shift_date)
            for i in range(size):
                start_time, end_time = shift_time[i].split("-")
                google_startdate = shift_date[i] + "T" + start_time + ":00+09:00"
                google_enddate = shift_date[i] + "T" + end_time + ":00+09:00"
                print(google_startdate)
                # Googleカレンダーに書き込むイベントデータを作成
                event_data = {
                    'summary': '予定名を入れる',  
                    'description': 'Shift details',
                    'start': {
                        'dateTime': google_startdate,
                        'timeZone': 'Asia/Tokyo',
                    },
                    'end': {
                        'dateTime': google_enddate,
                        'timeZone': 'Asia/Tokyo',
                    },
                }

                # Googleカレンダーにイベントを追加
                credentials = service_account.Credentials.from_service_account_file(key.service_account_file, scopes=['https://www.googleapis.com/auth/calendar'])
                endtime = start_time + ":00+09:00"
                if google_calendar.check_duplicate_events(key.calendar_id, credentials, google_startdate, google_enddate, shift_date[i],endtime) == True:
                    continue
                google_calendar.add_event_to_calendar(key.calendar_id, credentials, event_data)
        send_mail.send_email()
