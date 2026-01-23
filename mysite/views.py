from django.http import Http404, HttpResponse
from datetime import datetime, timedelta, date
from django.template.loader import get_template
from django.shortcuts import render

'''
#~~~SESSION 1~~~#

#session 1 exercise 1.1
def hello(request):
    return HttpResponse("Hello, world")

#session 1 exercise 1.2

def current_datetime(request):
    now = datetime.datetime.now()
    html = "<html><body>It is now %s.</body></html>" % now
    return HttpResponse(html)


#session 1 exercise 1.3
def hours_ahead(request, offset):
  try:
      offset = int(offset)
  except ValueError:
      raise Http404()
  dt = datetime.datetime.now() + datetime.timedelta(hours=offset)
  html = f"<html><body>In {offset} hour(s), it will be {dt}.</body></html>"
  return HttpResponse(html)

#session 1exercise 2.1
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

#session 1exercise 2.2
def valid_date(request, year: int, month: int, day: int):
    try:
        date(year, month, day)
        return HttpResponse(f"The date {year}-{month}-{day} is valid!")
    except ValueError:
        return HttpResponse(f"The date {year}-{month}-{day} is NOT valid!")

'''

#~~~SESSION 2~~~#

#session 2 with template

def home(request):
    return render(request, "base.html") 

def current_datetime(request):
    now = datetime.now()
    return render(
        request,
        "current_datetime.html",
        {"current_date": now},
    )

# session 2 exercise 1.3 
def hours_ahead(request, offset: int):
    now = datetime.now()
    next_time = now + timedelta(hours=offset)

    return render(
        request,
        "hours_ahead.html",
        {
            "hour_offset": offset,
            "current_time": now,
            "next_time": next_time,
        }
    )

# session 2 exercise 2.1
def math(request, number1: int, number2: int, number3: int = None):
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

    return render(
        request,
        "math.html",
        {
            "numbers": numbers,
            "sum": sum_result,
            "difference": diff_result,
            "product": prod_result,
            "quotient": quot_result,
        }
    )

# session 2 exercise 2.2 (templated)
def valid_date(request, year: int, month: int, day: int):
    try:
        date(year, month, day)
        is_valid = True
    except ValueError:
        is_valid = False

    return render(
        request,
        "valid_date.html",
        {
            "year": year,
            "month": month,
            "day": day,
            "is_valid": is_valid,
        }
    )
