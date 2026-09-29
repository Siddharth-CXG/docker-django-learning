from django.test import TestCase
from django.urls import reverse

from .models import ContactMessage


class HomePageTests(TestCase):
	def test_home_displays_title_and_placeholder_statistics(self):
		response = self.client.get(reverse('home'))

		self.assertEqual(response.status_code, 200)
		self.assertContains(response, '<h1 id="page-title">Energy Dashboard</h1>', html=True)
		self.assertContains(response, 'Total Assets')
		self.assertContains(response, 'Active Assets')
		self.assertContains(response, 'Alerts')
		self.assertContains(response, '4')
		self.assertContains(response, '3')
		self.assertContains(response, '1')

	def test_main_navigation_routes_respond(self):
		for route_name in ('home', 'assets', 'about', 'contact'):
			with self.subTest(route=route_name):
				response = self.client.get(reverse(route_name))
				self.assertEqual(response.status_code, 200)

		response = self.client.get(reverse('home'))
		for route_name in ('home', 'assets', 'about', 'contact'):
			with self.subTest(link=route_name):
				self.assertContains(response, f'href="{reverse(route_name)}"')


class AssetPageTests(TestCase):
	def test_assets_page_lists_four_assets_with_required_types(self):
		response = self.client.get(reverse('assets'))

		self.assertEqual(response.status_code, 200)
		self.assertEqual(len(response.context['assets']), 4)
		self.assertEqual(
			{asset['type'] for asset in response.context['assets']},
			{'Solar PV', 'Wind', 'Battery Storage'},
		)
		for asset_name in (
			'Sunrise Solar Array',
			'North Ridge Wind Farm',
			'Harbor Battery',
			'East Field Solar',
		):
			with self.subTest(asset=asset_name):
				self.assertContains(response, asset_name)


class AboutPageTests(TestCase):
	def test_about_page_explains_django_and_docker_learning_purpose(self):
		response = self.client.get(reverse('about'))

		self.assertEqual(response.status_code, 200)
		self.assertContains(response, 'Django application')
		self.assertContains(response, 'containerisation with Docker')


class ContactPageTests(TestCase):
	def test_contact_page_shows_required_fields(self):
		response = self.client.get(reverse('contact'))

		self.assertEqual(response.status_code, 200)
		self.assertContains(response, 'name="name"')
		self.assertContains(response, 'name="email"')
		self.assertContains(response, 'name="message"')
		self.assertContains(response, 'csrfmiddlewaretoken')

	def test_invalid_submission_shows_errors_and_preserves_values(self):
		response = self.client.post(
			reverse('contact'),
			{'name': '  Taylor  ', 'email': 'not-an-email', 'message': '  Hello  '},
		)

		self.assertEqual(response.status_code, 200)
		self.assertContains(response, 'Enter a valid email address.')
		self.assertContains(response, 'value="  Taylor  "')
		self.assertContains(response, '  Hello  ')
		self.assertEqual(ContactMessage.objects.count(), 0)
		self.assertNotContains(response, 'Your message has been saved.')

	def test_valid_submission_is_trimmed_saved_and_confirmed(self):
		response = self.client.post(
			reverse('contact'),
			{'name': '  Taylor  ', 'email': 'taylor@example.com', 'message': '  Hello  '},
		)

		self.assertEqual(response.status_code, 200)
		self.assertContains(response, 'Your message has been saved.')
		self.assertEqual(ContactMessage.objects.count(), 1)
		message = ContactMessage.objects.get()
		self.assertEqual(message.name, 'Taylor')
		self.assertEqual(message.email, 'taylor@example.com')
		self.assertEqual(message.message, 'Hello')


class HealthEndpointTests(TestCase):
	def test_health_returns_healthy_json(self):
		response = self.client.get(reverse('health'))

		self.assertEqual(response.status_code, 200)
		self.assertEqual(response['Content-Type'], 'application/json')
		self.assertEqual(response.json(), {'status': 'healthy'})
