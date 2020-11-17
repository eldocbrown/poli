from django.test import TestCase, Client

# Create your tests here.
class TestUrls(TestCase):

    def test_default_route_return_http200(self):
        c = Client()
        response = c.post(f"/")
        self.assertEqual(response.status_code, 200)

    def test_default_route_render_index(self):
        c = Client()
        response = c.post(f"/")
        self.assertTemplateUsed(response, 'policon/index.html')

if __name__ == "__main__":
    unittest.main()
