
# 需要用pip安装watchdog库
# 注意要修改谷歌账号的安全性设置，要生成App passwords，而且还要开启两步验证
# 代码建议不要在虚拟机环境下运行，虚拟机下检测不到文件变化

import time
import smtplib
import os
import mimetypes
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from email.message import EmailMessage

# 配置邮件发送信息
# 这个是发送者邮箱
EMAIL_ADDRESS = '建议使用谷歌邮箱'
# 这个是发送者邮箱的App passwords（生成的）
EMAIL_PASSWORD = '谷歌的app passwords，需要先开启两步验证'

#这两行固定
SMTP_SERVER = 'smtp.gmail.com'
SMTP_PORT = 587  # 常用端口是587或465

# 配置接收者邮箱
TO_ADDRESS = '接收者邮箱'

class AnyFileHandler(FileSystemEventHandler):
    def on_any_event(self, event):
        # 输出所有事件和相关路径以帮助调试
        print(f"触发事件：{event.event_type}，路径：{event.src_path}")

    def on_created(self, event):
        if not event.is_directory:
            print(f"检测到新文件：{event.src_path}")
            self.send_email(event.src_path)

    def send_email(self, filepath):
        msg = EmailMessage()
        msg['Subject'] = '新图片通知'
        msg['From'] = EMAIL_ADDRESS
        msg['To'] = TO_ADDRESS
        msg.set_content('有一张新图片添加到监控文件夹。')

        # 使用 mimetypes 模块检测文件的 MIME 类型
        ctype, encoding = mimetypes.guess_type(filepath)
        if ctype is None or encoding is not None:
            # 如果无法检测，使用默认的二进制流类型
            ctype = 'application/octet-stream'
        maintype, subtype = ctype.split('/', 1)

        try:
            with open(filepath, 'rb') as f:
                file_data = f.read()
                file_name = os.path.basename(filepath)
            msg.add_attachment(file_data, maintype=maintype, subtype=subtype, filename=file_name)
        except Exception as e:
            print(f"读取文件时发生错误: {e}")
            return

        try:
            with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as smtp:
                smtp.ehlo()
                smtp.starttls()
                smtp.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
                smtp.send_message(msg)
            print(f'已发送 {file_name} 到 {TO_ADDRESS}')
        except smtplib.SMTPAuthenticationError as e:
            print(f'SMTP认证失败: {e}')
        except Exception as e:
            print(f'发送邮件时发生错误: {e}')

if __name__ == "__main__":
    # 这里注意地址格式，windows/linux
    path = '这个是你本地监控的文件夹'  # 确保这是一个有效且有权限访问的路径
    event_handler = AnyFileHandler()
    observer = Observer()
    observer.schedule(event_handler, path, recursive=True)
    observer.start()
    print(f'开始监控 {path} 文件夹...')
    try:
        while True:
            time.sleep(10)  # 增加循环延时来减少资源消耗
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
