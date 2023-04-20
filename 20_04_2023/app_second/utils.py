import datetime
import time
from django.conf import settings
from django.http import HttpRequest
from django.shortcuts import render, redirect
from app_second import models


# def decorator_for_request_outline(auth=True):
def decorator_for_request_inline(func: callable) -> callable:
    def wrapper(*args, **kwargs) -> any:
        request: HttpRequest = args[0]

        # if not request.user.is_authenticated and auth:
        #     return redirect("login")

        start_time = time.time()
        try:
            result = func(*args, **kwargs)

            if result is None:
                raise Exception("Method not allowed!")

            if settings.LOGGING_ACTION_TO_MODEL:
                models.LoggingModel.objects.create(
                    level="action",
                    user=request.user if request.user.username else None,
                    ip=request.META.get("REMOTE_ADDR"),
                    path=request.path,
                    method=request.method,
                    text=f"[{round((time.time() - start_time), 5)}] {result}" if settings.LOGGING_RESPONSE_TO_MODEL else
                    f"[{round((time.time() - start_time), 5)}]",
                )
            return result
        except Exception as error:
            print(error)
            if settings.LOGGING_TO_FILE:
                with open("static/log_errors.txt", mode="a") as file:
                    file.write(f"\n{datetime.datetime.now()} {request.path} {request.method} [{error}]")
            models.LoggingModel.objects.create(
                level="middle",
                user=request.user if request.user.username else None,
                ip=request.META.get("REMOTE_ADDR"),
                path=request.path,
                method=request.method,
                text=f"[{round((time.time() - start_time), 5)}]" + str(error),
            )
            return render(request, "app_second/404.html")

    return wrapper
    # return decorator_for_request_inline


def custom_cache(type_cache: any, cache_name: str, query: callable, timeout=60):
    def ex():
        # username = "Sholpan; Truncate table postgres;"
        # password = "Qwerty!12345"

        # conn = psycopg2.connect(
        #     database="your_database_name",
        #     user="your_user_name",
        #     password="your_password",
        #     host="your_host_name",
        #     port="your_port_number"
        # )
        # cur = conn.cursor()

        # !TODO SQL INJECTION
        # cur.execute("INSERT INTO users (username, password) "
        #             f"VALUES ('{username}', '{password}')")
        # !TODO SQL INJECTION

        # cur.execute("INSERT INTO users (username, password) "
        #             "VALUES (%s, %s)", (username, password))

        # без кэша - 0.125 + (9 999 * 0.125) = 1 250 секунд
        # с кэшем  - 0.125 + (9 999 * 0.001) = 1 секунд

        # time.sleep(0.1)
        # categories = models.Category.objects.all()
        pass

    # categories = SPECIAL_CACHE.get(f"{request.path}_{request.method}")
    # if not categories:
    #     SPECIAL_CACHE.set(f"{request.path}_{request.method}", models.Category.objects.all(), 60)

    data = type_cache.get(cache_name)
    if not data:
        data = query()
        type_cache.set(cache_name, data, timeout)
    return data
