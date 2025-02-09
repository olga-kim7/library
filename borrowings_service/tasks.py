import os
import time

import django
from celery import shared_task

import requests
import logging
from django.utils import timezone

from django.conf import settings
from Library.celery import app
from borrowings_service.models import Borrowing, Payment

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "Library.settings")

django.setup()

logger = logging.getLogger(__name__)

TELEGRAM_BOT_TOKEN = settings.TELEGRAM_BOT_TOKEN
TELEGRAM_CHAT_ID = settings.TELEGRAM_CHAT_ID
TELEGRAM_API_URL = (f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/"
                    f"sendMessage")


@shared_task
def send_telegram_message(message: str):
    """Надсилає повідомлення у Telegram"""
    try:
        response = requests.post(
            TELEGRAM_API_URL,
            data={"chat_id": TELEGRAM_CHAT_ID, "text": message},
        )
        response.raise_for_status()
        logger.info(f"Telegram message sent: {message}")
    except requests.exceptions.RequestException as e:
        logger.error(f"Failed to send Telegram message: {e}")


@shared_task
def notify_new_borrowing(borrowing_id: int):
    try:
        borrowing = Borrowing.objects.get(id=borrowing_id)
        message = (
            f" New Borrowing!\n"
            f"User: {borrowing.user_id.email}\n"
            f"Book: {borrowing.book_id.title}\n"
            f"Borrow Date: {borrowing.borrowing_date}\n"
            f"Due Date: {borrowing.expected_date}"
        )
        send_telegram_message(message)
    except Borrowing.DoesNotExist:
        logger.error(f"Borrowing with id {borrowing_id} does not exist.")


@shared_task
def notify_overdue_borrowings():
    """Щоденне сповіщення про прострочені книги"""
    today = timezone.now().date()
    overdue_borrowings = Borrowing.objects.filter(
        expected_date__lt=today, actual_return__isnull=True
    )

    if overdue_borrowings.exists():
        message = "Overdue Borrowings!\n"
        for borrowing in overdue_borrowings:
            days_overdue = (today - borrowing.expected_date).days
            message += (f" {borrowing.book_id.title} - "
                        f"{borrowing.user_id.email}"
                        f"({days_overdue} days overdue)\n")
    else:
        message = "No overdue borrowings today!"

    send_telegram_message(message)


@shared_task
def notify_successful_payment(payment_id: int):
    """Сповіщення про успішну оплату"""
    try:
        payment = Payment.objects.get(id=payment_id)
        message = (
            f"Payment Received!\n"
            f"User: {payment.borrowing_id.user_id.email}\n"
            f"Book: {payment.borrowing_id.book_id.title}\n"
            f"Amount: ${payment.money_to_pay}\n"
            f"Status: {payment.status}"
        )
        send_telegram_message(message)
    except Payment.DoesNotExist:
        logger.error(f"Payment with id {payment_id} does not exist.")
