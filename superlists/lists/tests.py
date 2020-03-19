# Unit Test, and How They differ from Functional Tests
# Functional tests test the application from the outside, from the
# point of view of the user.
# Unit tests test the application from the inside, from the point of
# view of the programmer.

# TDD approach workflow for our application
# 1. We start by writing a functional test, describing the new
#   functionality from the user's point of view.
# 2. Once we have a functional test that fails, we start to think
#   about how to write code that can get it to pass (or at least to
#   get past its current failure). We now use one or more unit tests
#   to define how we want our code to behave -- the idea is that each
#   line of production code we write should be tested by (at least)
#   one of our unit tests.
# 3. Once we have a failing unit test, we write the smallest amount
#   of application code we can, just enough to get the unit test to
#   pass. We may iterate between step 2 and 3 a few times, until we
#   think the functional test will get a litle further.
# 4. Now we can rerun our functional tests and see if they pass, or
#   get a little further. That may prompt us to write some new unit
#   tests, and some new code, and so on.

# The functional tests are driving what development we do from a high
# level, while the unit tests drive what we do at a low level.

# Functional tests should help you build an application with the
# right functionality, and guarantee you never accidentally break it.
# Unit tests should help you to write code that's clean and bug free.

from django.test import TestCase


class SmokeTest(TestCase):

    def test_bad_maths(self):
        self.assertEqual(1 + 1, 3)
