import os
import sys

os.environ["DJANGO_SETTINGS_MODULE"] = "config.settings"
sys.path.append("..")

import django
import time  # 추가

django.setup()

# print("django.apps.ready : ", django.apps.ready)
# while not django.apps.ready:  # apps가 준비될 때까지 대기
#     time.sleep(10)

from pybo.models import Question
from django.utils import timezone

# django_configurations.setup()


for i in range(300):
    q = Question(subject=f"테스트 데이터 {i}", content="테스트", create_date=timezone.now())
    q.save()
