#!/usr/bin/env python
# coding=utf-8

import uuid


def get_mac_address():
    return uuid.uuid1().hex[-12:].upper()
