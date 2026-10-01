from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from complaints.models import Complaint, Notification, UserProfile


class ComplaintWorkflowTests(TestCase):
	def setUp(self):
		self.password = "StrongPass123!"
		self.user = User.objects.create_user(
			username="user@example.com",
			email="user@example.com",
			password=self.password,
		)
		UserProfile.objects.create(user=self.user, mobile_number="9876543210")

	def test_user_can_authenticate_with_email(self):
		response = self.client.post(reverse("login"), {
			"identifier": "user@example.com",
			"password": self.password,
		})

		self.assertRedirects(response, reverse("home"))
		self.assertTrue(response.wsgi_request.user.is_authenticated)

	def test_user_can_authenticate_with_mobile_number(self):
		response = self.client.post(reverse("login"), {
			"identifier": "9876543210",
			"password": self.password,
		})

		self.assertRedirects(response, reverse("home"))
		self.assertTrue(response.wsgi_request.user.is_authenticated)

	def test_authenticated_user_can_submit_complaint(self):
		self.client.force_login(self.user)

		response = self.client.post(reverse("submit_complaint"), {
			"title": "Broken street light",
			"category": "Street Light",
			"description": "The light has been off for three nights.",
			"state": "Karnataka",
			"city": "Bengaluru",
			"address": "12 Main Road",
			"zipcode": "560001",
			"priority": "High",
			"latitude": "12.9716",
			"longitude": "77.5946",
		})

		self.assertRedirects(response, reverse("dashboard"))
		complaint = Complaint.objects.get()
		self.assertEqual(complaint.title, "Broken street light")
		self.assertEqual(complaint.user, self.user)
		self.assertEqual(complaint.status, "Pending")

	def test_staff_can_mark_complaint_as_resolved(self):
		staff_user = User.objects.create_user(
			username="staff@example.com",
			email="staff@example.com",
			password=self.password,
			is_staff=True,
		)
		complaint = Complaint.objects.create(
			user=self.user,
			title="Pothole",
			category="Road",
			description="Large pothole near the school.",
			state="Karnataka",
			city="Bengaluru",
			address="School Road",
			zipcode="560001",
			priority="Medium",
		)
		self.client.force_login(staff_user)

		response = self.client.post(reverse("update_status", args=[complaint.id]), {
			"status": "Resolved",
		})

		self.assertRedirects(response, reverse("admin_dashboard"))
		complaint.refresh_from_db()
		self.assertEqual(complaint.status, "Resolved")
		self.assertTrue(Notification.objects.filter(
			user=self.user,
			message="Your complaint 'Pothole' status updated to Resolved",
		).exists())
