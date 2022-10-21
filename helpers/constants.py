import enum


class Messages(enum.Enum):
    EVENT_INVITE = 'Request for participation'
    EVENT_DECLINE = 'Cancellation of participation'
    REQUEST_CONFIRM = 'The request is confirmed'
    REQUEST_REJECTED = 'The request is rejected'


class EventNotification(enum.Enum):
    SUCCESS = 'Request success'
    NOT_SUCCESS = 'Request not successful'
