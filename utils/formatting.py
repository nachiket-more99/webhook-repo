from dateutil import parser

def format_event_timestamp(ts):
    if not ts:
        return None
    dt = parser.isoparse(ts)
    return dt.strftime("%d %B %Y - %I:%M %p UTC")