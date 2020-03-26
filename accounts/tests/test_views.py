from django.test import TestCase

import accounts.views


class SendLoginEmailViewTest(TestCase):

    def test_redirects_to_home_page(self):
        response = self.client.post(
            '/accounts/send_login_email',
            data={'email': 'edith@example.com'}
        )
        self.assertRedirects(response, '/')

    def test_sends_email_to_address_from_post(self):
        self.send_mail_called = False

        def fake_send_mail(subject, body, from_email, to_list):
            self.send_mail_called = True
            self.subject = subject
            self.body = body
            self.from_email = from_email
            self.to_list = to_list

        accounts.views.send_mail = fake_send_mail
        # It’s important to realise that there isn’t really anything
        # magical going on here; we’re just taking advantage of
        # Python’s dynamic nature and scoping rules.
        # Up until we actually invoke a function, we can modify the
        # variables it has access to, as long as we get into the
        # right namespace (that’s why we import the top-level
        # accounts module, to be able to get down to the accounts.
        # views module, which is the scope that the accounts.views.
        # send_login_email function will run in).

        self.client.post(
            '/accounts/send_login_email',
            data={'email': 'edith@example.com'}
        )

        self.assertTrue(self.send_mail_called)
        self.assertEqual(self.subject, 'Your login link for Superlists')
        self.assertEqual(self.from_email, 'noreply@superlists')
        self.assertEqual(self.to_list, ['edith@example.com'])
