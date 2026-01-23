from django.http import HttpResponse
from datetime import datetime, timedelta, date

#exercise 1
def hello(request):
    return HttpResponse("Hello, world")

#exercise 2
def current_datetime(request):
    now = datetime.datetime.now()
    html = "<html><body>It is now %s.</body></html>" % now
    return HttpResponse(html)

#exercise 3
def hours_ahead(request, offset: int):
    future_time = datetime.now() + timedelta(hours=offset)
    return HttpResponse(f"In {offset} hour(s), it will be {future_time} into the future")

#exercise 4.1
def math(request, number1: int, number2: int, number3: int=None):
    a, b = number1, number2
    c = number3
    numbers = [a, b] if c is None else [a, b, c]
    sum_result = sum(numbers)
    diff_result = a - b if c is None else a - b - c
    prod_result = a * b if c is None else a * b * c
    try:
        quot_result = a / b if c is None else a / b / c
    except ZeroDivisionError:
        quot_result = "undefined (division by zero)"

    return HttpResponse(
        f"Numbers: {numbers}<br>"
        f"Sum: {sum_result}<br>"
        f"Difference: {diff_result}<br>"
        f"Product: {prod_result}<br>"
        f"Quotient: {quot_result}"
    )

#exercise 4.2
def valid_date(request, year: int, month: int, day: int):
    try:
        date(year, month, day)
        return HttpResponse(f"The date {year}-{month}-{day} is valid!")
    except ValueError:
        return HttpResponse(f"The date {year}-{month}-{day} is NOT valid!")
