from datetime import date

DAILY_LIMIT = 20

_user_limits: dict[int, dict] = {}


def can_make_request(user_id: int) -> bool:
    today = date.today()

    data = _user_limits.get(user_id)

    if not data or data["date"] != today:
        _user_limits[user_id] = {
            "date": today,
            "count": 1
        }
        return True

    if data["count"] >= DAILY_LIMIT:
        return False

    data["count"] += 1
    return True


def requests_left(user_id: int) -> int:
    data = _user_limits.get(user_id)

    if not data:
        return DAILY_LIMIT

    return max(0, DAILY_LIMIT - data["count"])
