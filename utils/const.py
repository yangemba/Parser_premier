"""Constants variables for Premier Scraping"""

PAGE_INDICATOR = '?page='
RETRY_REQUEST_TIME = 3
RETRIES_QNT = 3

DATA_OFF_WORD_1 = 'день'
DATA_OFF_WORD_2 = 'дня'
DATA_OFF_WORD_3 = 'дней'

###########################################
"""Constants for handlers.

It's strongly recommended to do no changes in variables below.

Attributes:
    `HTTP_CODES` (dict): maps of HTTP status-codes and corresponding verbal
                         description;
"""

HTTP_CODES = {
    400: 'Bad Request',
    401: 'Unauthorized',
    402: 'Payment Required',
    403: 'Forbidden',
    404: 'Not Found',
    405: 'Method Not Allowed',
    406: 'Not Acceptable',
    409: 'Conflict',
    415: 'Unsupported Media Type',
    426: 'Upgrade Required',
    429: 'Too Many Requests',

    500: 'Internal Server Error',
    501: 'Not Implemented',
    503: 'Service Unavailable',
}



