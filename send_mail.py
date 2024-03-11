import smtplib, ssl
from email.mime.text import MIMEText
#上で作成したpyファイルから、account情報を読み込みます
import key
import datetime


# メインの関数になります
def send_email():
  msg = make_mime_text(
    mail_to = key.send_address,
    subject = "jobcan実行確認",
    body = str(datetime.datetime.today()) + "に実行済み\n",
  )
  send_gmail(msg)

# 件名、送信先アドレス、本文を渡す関数です
def make_mime_text(mail_to, subject, body):
  msg = MIMEText(body, "html")
  msg["Subject"] = subject
  msg["To"] = mail_to
  msg["From"] = key.account
  return msg

# smtp経由でメール送信する関数です
def send_gmail(msg):
  server = smtplib.SMTP_SSL(
    "smtp.gmail.com", 465,
    context = ssl.create_default_context())
  server.set_debuglevel(0)
  server.login(key.account, key.password)
  server.send_message(msg)
