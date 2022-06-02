from locust import HttpUser, TaskSet, task


def login(l):
    l.client.post("auth/login/", {"username": "django", "password": "123"})


def logout(l):
    l.client.post("auth/logout/", {"username": "django", "password": "123"})


def index(l):
    l.client.get("")


def products(l):
    l.client.get("products/")


@task
class UserBehavior(TaskSet):
    tasks = {login: 1, logout: 1}

    def on_start(self):
        login(self)

    def on_stop(self):
        logout(self)


@task
class WebsiteUser(HttpUser):
    task_set = UserBehavior
    min_wait = 5000
    max_wait = 9000
