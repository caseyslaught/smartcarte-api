from datetime import datetime, timezone


def get_utc_datetime_now():
    return datetime.utcnow().replace(tzinfo=timezone.utc)
