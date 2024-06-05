from django.test import TestCase
from django.core.files.uploadedfile import SimpleUploadedFile
from app.transducer.views import get_response, get_code
from app.testing.test_util import openfile, readfile
import re

'''This module tests for graceful error handling of invalid input to LaSer'''

TEST_FILES_FA = ["test_files/error/CombinedNotSubsetNFA.fa"]

class MyTestCase(TestCase):
    pass
