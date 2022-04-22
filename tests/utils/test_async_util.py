from unittest import IsolatedAsyncioTestCase, TestCase

from utils.async_util import async_wrap, run_async


class TestAsyncUtil(TestCase):
    def test_run_async(self):
        R = 1

        async def atest():
            return R
        r = run_async(atest())
        self.assertEquals(R, r)


class TestAsyncUtilAsync(IsolatedAsyncioTestCase):
    async def test_async_wrap(self):
        R = 1

        @async_wrap
        def syncfunc():
            return R

        r = await syncfunc()
        self.assertEquals(R, r)

    async def test_run_async(self):
        R = 1

        async def asyncfunc():
            return R
        r = run_async(asyncfunc())
        self.assertEquals(R, r)
