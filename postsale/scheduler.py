from django.dispatch import Signal
import schedule
import threading
import time
from .models import OutBound
from django.utils import timezone
from django.core.mail import send_mail

def check_overdue_pay_outbound():
    today_overdue_outbounds = OutBound.objects.filter(pay_state="unpaid").filter(pay_date=timezone.now().date())

    for outbounds in today_overdue_outbounds:
        operator = outbounds.outbound_operator
        outbound_number = outbounds.outbound_number
        subject = "未结算出库单到期提醒"
        message = f"出库单:{outbound_number} 今天是结算最后一天，请及时操作!"
        fromEmail = "admin@equipment_manager.com"
        recipants = [operator.email]
        send_mail(subject,message,fromEmail,recipants)


def check_periodically():
    schedule.every().day.at("07:00").do(check_overdue_pay_outbound)

    while True:
        schedule.run_pending()
        time.sleep(1)

def start_scheduler():
    t = threading.Thread(target=check_periodically)
    t.start()