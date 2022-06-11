#!/usr/bin/env python

from tests.classifier import run_test as test_classifier
from tests.ASCReader import run_test as test_asc_reader

test_classifier()
test_asc_reader()
