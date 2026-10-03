from django.test import TestCase
from django.contrib.auth.models import User
from complaints.models import Complaint


class ComplaintTrackingTests(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser",
            password="testpass123"
        )

    def test_user_can_login(self):
        response = self.client.login(
            username="testuser",
            password="testpass123"
        )
        self.assertTrue(response)

    def test_complaint_can_be_created(self):
        complaint = Complaint.objects.create(
            user=self.user,
            title="Test Complaint",
            description="Testing complaint submission and tracking."
        )

        self.assertEqual(complaint.user, self.user)
        self.assertEqual(complaint.status, "Pending")

    def test_complaint_status_can_be_updated(self):
        complaint = Complaint.objects.create(
            user=self.user,
            title="Tracking Test",
            description="Testing complaint status."
        )

        complaint.status = "In Progress"
        complaint.save()

        complaint.refresh_from_db()

        self.assertEqual(complaint.status, "In Progress")