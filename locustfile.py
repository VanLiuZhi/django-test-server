#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/10/7 下午10:46
# @Author  : liuzhi
# @File    : 5.py

from locust import HttpLocust, TaskSet, task


class UserBehavior(TaskSet):
    @task
    def sleep(self):
        self.client.post("/work")

    # @task
    # def sleep2(self):
    #     self.client.get("/work")


class WebsiteUser(HttpLocust):
    task_set = UserBehavior
    min_wait = 0  # 单位 ms 请求等待的最小时间
    max_wait = 1

# locust --host=http://localhost:8888
