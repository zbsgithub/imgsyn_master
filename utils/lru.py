#!/usr/bin/env python
# coding=utf-8

import threading


class _Node(object):

    def __init__(self, key, val, next=None, pre=None):
        self.key = key
        self.val = val
        self.next = next
        self.pre = pre

    def __str__(self):
        return self.key


class _LinkList(object):

    def __init__(self):
        self._head = None
        self._tail = None

    def remove(self, node):
        pre = node.pre
        next = node.next
        if pre:
            pre.next = next
        else:
            self._head = next
        if next:
            next.pre = pre
        else:
            self._tail = pre

    def remove_tail(self):
        tail = self._tail
        if self._head == self._tail:
            self._head = None
            self._tail = None
        pre = self._tail.pre
        self._tail = pre
        self._tail.next = None
        return tail

    def push_front(self, node):
        head = self._head
        if head:
            head.pre = node
        else:
            self._tail = node
        node.pre = None
        node.next = head
        self._head = node

    def printf(self):
        node = self._head
        str = u"%s %s | " % (self._head, self._tail)
        while node:
            # str += node.key + u":" + node.val + u" --> "
            str += node.key + u" --> "
            node = node.next
        print
        "linklist:", str


class LruCache(object):

    def __init__(self, maxsize):
        self._maxsize = maxsize
        self._dict_data = {}
        self._linklist = _LinkList()
        self._lock = threading.Lock()

    def get(self, key):
        with self._lock:
            node = self._dict_data.get(key)
            if not node:
                return None
            val = node.val
            self._linklist.remove(node)
            self._linklist.push_front(node)
            return val

    def set(self, key, val):
        with self._lock:
            node = self._dict_data.get(key)
            if node:
                self._linklist.remove(node)
            else:
                node = _Node(key, val, None, None)
                self._dict_data[key] = node
            self._linklist.push_front(node)
            if len(self._dict_data) > self._maxsize:
                delete_node = self._linklist.remove_tail()
                try:
                    del self._dict_data[delete_node.key]
                except:
                    pass

    def __len__(self):
        return len(self._dict_data)

    def printf(self):
        self._linklist.printf()


if __name__ == "__main__":
    import random
    import time
    from utils.qqwry import IPInfo

    ipinfo = IPInfo("../app_data/qqwry.dat")
    cache = LruCache(500000)
    ipstrs = []
    for index in range(0, 10000):
        ipstr = "%s.%s.%s.%s" % (
            random.randint(0, 255),
            random.randint(0, 255),
            random.randint(0, 255),
            random.randint(0, 255)
        )
        ipstrs.append(ipstr)

    count = 0
    find_count = 0
    begin_time = time.time()
    while True:
        ipstr = "%s.%s.%s.%s" % (
            random.randint(0, 255),
            random.randint(0, 255),
            random.randint(0, 255),
            random.randint(0, 255)
        )
        # ipstr = random.choice(ipstrs)
        address = cache.get(ipstr)
        if not address:
            (c, address) = ipinfo.get_ip_addr(ipstr)
            cache.set(ipstr, address)
            # print ipstr, c, address, len(cache)
        else:
            find_count += 1
            # print ipstr, None, address, len(cache)
            """
            (c, address1) = ipinfo.get_ip_addr(ipstr)
            if address != address1:
                raise Exception("fatal error")
            """
        """
        cache.printf()
        print "\n"
        time.sleep(2)
        """
        count += 1
        if count == 10000000000000:
            break
    end_time = time.time()
    print
    end_time - begin_time, find_count, count / (end_time - begin_time)
