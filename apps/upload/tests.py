# tests.py
from io import BytesIO
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase
from django.urls import reverse

class FileUploadTestCase(TestCase):

    def generate_text_file(self, size_in_kb):
        """Generates a text file of a given size (in KB)."""
        content = b"A" * (size_in_kb * 1024)
        file = BytesIO(content)
        return file

    def test_file_upload_less_than_5MB(self):
        """Test file upload of a file less than 5MB."""
        file_io = self.generate_text_file(4000)
        file = SimpleUploadedFile("small_file.txt", file_io.read())

        response = self.client.post(reverse('file_upload'), {'file': file})

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "File uploaded: small_file.txt")

    def test_file_upload_greater_than_5MB(self):
        """Test file upload of a file greater than 5MB."""
        file_io = self.generate_text_file(5100)
        file = SimpleUploadedFile("large_file.txt", file_io.read())
        response = self.client.post(reverse('file_upload'), {'file': file})

        self.assertNotEqual(response.status_code, 200)
