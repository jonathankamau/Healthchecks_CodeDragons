from django.contrib.auth.hashers import make_password
from hc.test import BaseTestCase


class CheckTokenTestCase(BaseTestCase):

    def setUp(self):
        super(CheckTokenTestCase, self).setUp()
        self.profile.token = make_password("secret-token")
        self.profile.save()

    def test_it_shows_form(self):
        r = self.client.get("/accounts/check_token/alice/secret-token/")
        self.assertContains(r, "You are about to log in")

    def test_it_redirects(self):
        r = self.client.post("/accounts/check_token/alice/secret-token/")
        self.assertEqual(r.status_code, 302)
        # self.assertIn(self.profile.user, self.client.session)
        self.assertRedirects(r, "/checks/")

        # After login, token should be blank
        self.profile.refresh_from_db()
        self.assertEqual(self.profile.token, "")

    ### Login and test it redirects already logged in

    ### Login with a bad token and check that it redirects
    def test_redirects_login_with_bad_token(self):
        r = self.client.post("/accounts/check_token/alice/bad-token/")
        self.assertRedirects(r,"/accounts/login/")

    ### Any other tests?
