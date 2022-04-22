from datetime import datetime
import json
from unittest import TestCase
from cache.encoder import BaseClazzEncoder, WithInfoEncoder

from crawlers.c_model import CArea, CBase, CWithInfo
from tests.cache.mock_dbutil import random_str


def mock_base(c=CBase):
    d = datetime(2020, 1, 1)
    b = c()
    # cannot set objectId
    b._created_at = d
    b._updated_at = d
    return b, {"objectId": None, "createdAt": "2020-01-01T00:00:00",
               "updatedAt": "2020-01-01T00:00:00"}


def mock_wi(c=CWithInfo):
    w, DUMP = mock_base(c)
    w.rid = random_str()
    w.name = random_str()
    DUMP = {'objectId': None, "createdAt": "2020-01-01T00:00:00",
            "updatedAt": "2020-01-01T00:00:00", "rid": w.rid, "name": w.name}
    return w, DUMP


class TestEncoder(TestCase):
    def test_baseclazz_encoder(self):
        d, DUMP = mock_base()
        dump = json.dumps(d, cls=BaseClazzEncoder)
        self.assertDictEqual(dump, DUMP)

    def test_withinfo_encoder(self):
        w, DUMP = mock_wi()
        dump = json.loads(json.dumps(w, cls=WithInfoEncoder))
        self.assertDictEqual(dump, DUMP)

    def test_area_encoder(self):
        a, DUMP = mock_wi(CArea)
        dump = json.loads(json.dumps(a, cls=WithInfoEncoder))
        self.assertDictEqual(dump, DUMP)
