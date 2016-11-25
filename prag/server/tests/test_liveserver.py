from django import test
from django.conf import settings


@test.tag('liveserver')
@test.override_settings(TESTING=True)
class LiveServerTest(test.LiveServerTestCase):
    def test_liveserver(self):
        if settings.TEST_LIVESERVER:
            # use newline to force prompt printing in honcho
            input('Hit Enter to end liveserver...\n')
