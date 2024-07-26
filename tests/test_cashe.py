import pytest
import time
from cache.app import app, add, add_pro, del_add_cache, del_pro_cache


@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client


def test_index(client):
    res = client.get('/')
    assert res.status_code == 200
    assert b"to simulate a poor server or heavy work." in res.data


def test_foo(client):
    url = '/foo'
    start_time = time.time()
    res = client.get(url)
    end_time = time.time()
    duration = end_time - start_time

    assert res.status_code == 200
    assert b'Without cache, the page will need more than 1 second (1000.00ms) to load, every time.' in res.data
    assert 1 <= duration < 2


def test_bar(client):
    url = '/bar'
    start_time = time.time()
    res = client.get(url)
    end_time = time.time()
    duration = end_time - start_time

    assert res.status_code == 200
    assert b'Bar' in res.data
    assert b'With cache enabled, only first load will need more than 1 second (1000.00ms).' in res.data
    assert 1 <= duration < 2

    start_time = time.time()
    res = client.get(url)
    end_time = time.time()
    duration = end_time - start_time

    assert res.status_code == 200
    assert duration < 1


def test_baz(client):
    url = '/baz'
    res = client.get(url)
    assert res.status_code == 200
    assert b'Baz' in res.data
    assert b'With cache enabled, only first load will need more than 1 second (1000.00ms).' in res.data


def test_qux(client):
    url = '/qux?page='
    start_time = time.time()
    res = client.get(url + '2')
    end_time = time.time()
    duration = end_time - start_time

    assert res.status_code == 200
    assert b'Qux' in res.data
    assert b"page: 2" in res.data
    assert 1 <= duration < 2

    start_time2 = time.time()
    res = client.get(url + '10')
    end_time2 = time.time()
    duration2 = end_time2 - start_time2

    assert res.status_code == 200
    assert duration2 >= 1


def test_bar_del_cache(client):
    url = '/update/bar'
    res = client.get(url)
    assert res.status_code == 302


def test_update_bar(client):
    url = '/update/bar'
    res = client.get(url, follow_redirects=True)
    assert res.status_code == 200
    assert b'Cached data for bar have been deleted.' in res.data


def test_update_baz(client):
    url = '/update/baz'
    res = client.get(url, follow_redirects=True)
    assert res.status_code == 200
    assert b'Cached data for baz have been deleted.' in res.data


def test_update_all(client):
    url = '/update/all'
    res = client.get(url, follow_redirects=True)
    assert res.status_code == 200
    assert b'All cached data deleted.' in res.data

    url = '/bar'
    start_time = time.time()
    res = client.get(url)
    end_time = time.time()
    duration = end_time - start_time
    assert 1 <= duration < 2


def test_add_caching(client):
    start_time = time.time()
    result1 = add(2, 3)
    end_time = time.time()
    duration1 = end_time - start_time

    assert result1 == 5
    assert 2 <= duration1 < 3

    start_time = time.time()
    result2 = add(2, 3)
    end_time = time.time()
    duration2 = end_time - start_time

    assert result2 == 5
    assert duration2 < 1

    del_add_cache()
    start_time = time.time()
    result3 = add(2, 3)
    end_time = time.time()
    duration3 = end_time - start_time

    assert result3 == 5
    assert 2 <= duration3 < 3


def test_add_pro_caching(client):
    start_time = time.time()
    result1 = add_pro(2, 3)
    end_time = time.time()
    duration1 = end_time - start_time

    assert result1 == 5
    assert 2 <= duration1 < 3

    start_time = time.time()
    result2 = add_pro(2, 3)
    end_time = time.time()
    duration2 = end_time - start_time

    assert result2 == 5
    assert duration2 < 1

    del_pro_cache()
    start_time = time.time()
    result3 = add_pro(2, 3)
    end_time = time.time()
    duration3 = end_time - start_time

    assert result3 == 5
    assert 2 <= duration3 < 3
# from cache.app import app, add, add_pro, del_add_cache, del_pro_cache
# import unittest
# import time


# class TestCache(unittest.TestCase):
#     def setUp(self):
#         self.app = app.test_client()
#         self.app.testing = True

#     def test_index(self):
#         res = self.app.get('/')
#         assert res.status_code == 200
#         self.assertIn(
#             b"to simulate a poor server or heavy work.", res.data)

#     def test_foo(self):  # test for no cache
#         url = '/foo'
#         start_time = time.time()
#         res = self.app.get(url)
#         end_time = time.time()
#         duration = end_time - start_time

#         assert res.status_code == 200
#         self.assertIn(
#             b'Without cache, the page will need more than 1 second (1000.00ms) to load, every time.', res.data)
#         self.assertTrue(1 <= duration < 2)

#     def test_bar(self):  # test for cache
#         url = '/bar'
#         # check the first load takes 1 second
#         start_time = time.time()
#         res = self.app.get(url)
#         end_time = time.time()
#         duration = end_time - start_time

#         assert res.status_code == 200
#         self.assertIn(b'Bar', res.data)
#         self.assertIn(
#             b'With cache enabled, only first load will need more than 1 second (1000.00ms).', res.data)
#         self.assertTrue(1 <= duration < 2)

#         # check second load takes less than a second
#         start_time = time.time()
#         res = self.app.get(url)
#         end_time = time.time()
#         duration = end_time - start_time

#         assert res.status_code == 200
#         self.assertTrue(duration < 1)

#     def test_baz(self):  # test for cache
#         url = '/baz'
#         res = self.app.get(url)
#         # check the first load takes 1 second
#         assert res.status_code == 200
#         self.assertIn(b'Baz', res.data)
#         self.assertIn(
#             b'With cache enabled, only first load will need more than 1 second (1000.00ms).', res.data)

#     def test_qux(self):  # test for cache with query string
#         url = '/qux?page='
#         # check the first load takes 1 second
#         start_time = time.time()
#         res = self.app.get(url+'2')
#         end_time = time.time()
#         duration = end_time - start_time

#         assert res.status_code == 200
#         self.assertIn(b'Qux', res.data)
#         self.assertIn(
#             b"page: 2", res.data)
#         self.assertTrue(1 <= duration < 2)

#         # check different query
#         start_time2 = time.time()
#         res = self.app.get(url+'10')
#         end_time2 = time.time()
#         duration2 = end_time2 - start_time2

#         assert res.status_code == 200
#         self.assertFalse(duration2 < 1)

#     def test_bar_del_cache(self):
#         url = '/update/bar'
#         res = self.app.get(url)
#         assert res.status_code == 302

#     def test_update_bar(self):
#         url = '/update/bar'
#         res = self.app.get(url, follow_redirects=True)
#         assert res.status_code == 200
#         self.assertIn(b'Cached data for bar have been deleted.', res.data)

#     def test_update_baz(self):
#         url = '/update/baz'
#         res = self.app.get(url, follow_redirects=True)
#         assert res.status_code == 200
#         self.assertIn(b'Cached data for baz have been deleted.', res.data)

#     def test_update_all(self):
#         url = '/update/all'
#         res = self.app.get(url, follow_redirects=True)
#         assert res.status_code == 200
#         self.assertIn(b'All cached data deleted.', res.data)

#         url = '/bar'
#         start_time = time.time()
#         res = self.app.get(url)
#         end_time = time.time()
#         duration = end_time - start_time
#         self.assertTrue(1 <= duration < 2)

#     def test_add_caching(self):
#         # Measure time for the first call
#         start_time = time.time()
#         result1 = add(2, 3)
#         end_time = time.time()
#         duration1 = end_time - start_time

#         # Ensure the first call takes about 2 seconds
#         assert result1 == 5
#         self.assertTrue(2 <= duration1 < 3)

#         # Measure time for the second call (should be cached)
#         start_time = time.time()
#         result2 = add(2, 3)
#         end_time = time.time()
#         duration2 = end_time - start_time

#         # Ensure the second call is almost instant due to caching
#         assert result2 == 5
#         self.assertTrue(duration2 < 1)

#         # Invalidate the cache and measure time for the call again
#         del_add_cache()
#         start_time = time.time()
#         result3 = add(2, 3)
#         end_time = time.time()
#         duration3 = end_time - start_time

#         # Ensure the cache is invalidated and the call takes about 2 seconds again
#         assert result3 == 5
#         self.assertTrue(2 <= duration3 < 3)

#     def test_add_pro_caching(self):
#         # Measure time for the first call
#         start_time = time.time()
#         result1 = add_pro(2, 3)
#         end_time = time.time()
#         duration1 = end_time - start_time

#         # Ensure the first call takes about 2 seconds
#         assert result1 == 5
#         self.assertTrue(2 <= duration1 < 3)

#         # Measure time for the second call (should be cached)
#         start_time = time.time()
#         result2 = add_pro(2, 3)
#         end_time = time.time()
#         duration2 = end_time - start_time

#         # Ensure the second call is almost instant due to caching
#         assert result2 == 5
#         self.assertTrue(duration2 < 1)

#         # Invalidate the memorized cache and measure time for the call again
#         del_pro_cache()
#         start_time = time.time()
#         result3 = add_pro(2, 3)
#         end_time = time.time()
#         duration3 = end_time - start_time

#         # Ensure the cache is invalidated and the call takes about 2 seconds again
#         assert result3 == 5
#         self.assertTrue(2 <= duration3 < 3)
