from telethon import events
from yandisk import client, admin

def message(**args):
    pattern = args.get('pattern', None)
    from_users = args.get('from_users', None)

    if pattern is not None and not pattern.startswith('(?i)'):
        args['pattern'] = '(?i)' + pattern
    elif from_users is not None:
        args["from_users"] = [admin]

    def decorator(func):
        [client.add_event_handler(func, events.NewMessage(**args))]
        [client.add_event_handler(func, events.MessageEdited(**args))]
        return func

    return decorator