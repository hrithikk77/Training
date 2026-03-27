import asyncio
import logging

# Simulating async notifications (Requirement 3)
async def send_email_async(user_email, message):
    await asyncio.sleep(1) # simulate network
    logging.info(f"Email sent to {user_email}")

async def send_sms_async(phone, message):
    await asyncio.sleep(1)
    logging.info(f"SMS sent to {phone}")

async def notify_all(email, phone, message):
    # Runs them concurrently
    await asyncio.gather(
        send_email_async(email, message),
        send_sms_async(phone, message)
    )