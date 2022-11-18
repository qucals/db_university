import enum


class user_type(enum.Enum):
    freelancer = 'freelancer',
    client = 'client'


class specialization(enum.Enum):
    maths = 'maths',
    programming = 'programming'


class order_type(enum.Enum):
    maths = 'maths',
    programming = 'programming'


class order_status(enum.Enum):
    opened = 'opened',
    in_progress = 'in_progress',
    under_warranty = 'under_warranty',
    closed = 'closed',
    closed_with_compensation = 'closed_with_compensation'


class operation_type(enum.Enum):
    withdraw = 'withdraw',
    top_up = 'top_up',
    freezing = 'freezing'
