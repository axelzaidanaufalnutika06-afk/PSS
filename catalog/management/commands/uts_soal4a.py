"""UTS PSS - Soal 4a: buat/pastikan data minimal tersedia.
Jalankan: docker compose exec app python manage.py uts_soal4a
"""
from datetime import timedelta

from django.core.management.base import BaseCommand
from django.utils import timezone

from catalog.models import Assignment, Course, Enrollment, Lesson, Submission
from users.models import User


class Command(BaseCommand):
    help = "Soal 4a: membuat data minimal (idempotent, aman dijalankan berulang)"

    def handle(self, *args, **options):
        dosen, _ = User.objects.get_or_create(
            username="suprayogi", defaults={"role": "LECTURER"})
        mhs1, _ = User.objects.get_or_create(
            username="fauzan", defaults={"role": "STUDENT"})
        mhs2, _ = User.objects.get_or_create(
            username="mahasiswa2", defaults={"role": "STUDENT"})

        c1, _ = Course.objects.get_or_create(
            code="PSS01",
            defaults={"title": "Pemrograman Sisi Server", "lecturer": dosen})
        Course.objects.get_or_create(
            code="BD01",
            defaults={"title": "Basis Data", "lecturer": dosen})

        for order, title in enumerate(
                ["Pengenalan Backend", "Pola Arsitektur Backend",
                 "Containerisasi dengan Docker"], start=1):
            Lesson.objects.get_or_create(
                course=c1, order=order,
                defaults={"title": title, "content": f"Isi materi {title}"})

        Enrollment.objects.get_or_create(student=mhs1, course=c1)
        Enrollment.objects.get_or_create(student=mhs2, course=c1)

        tugas, _ = Assignment.objects.get_or_create(
            course=c1, title="Tugas Django ORM",
            defaults={"description": "Implementasi model & relasi",
                      "deadline": timezone.now() + timedelta(days=7)})
        Submission.objects.get_or_create(
            assignment=tugas, student=mhs1,
            defaults={"content": "Jawaban saya", "grade": 87.5})

        self.stdout.write(self.style.SUCCESS("Data minimal Soal 4a siap:"))
        self.stdout.write(f"  Dosen       : {User.objects.filter(role='LECTURER', username='suprayogi').count()}")
        self.stdout.write(f"  Mahasiswa   : {User.objects.filter(username__in=['fauzan', 'mahasiswa2']).count()}")
        self.stdout.write(f"  Course      : {Course.objects.filter(code__in=['PSS01', 'BD01']).count()}")
        self.stdout.write(f"  Lesson PSS01: {Lesson.objects.filter(course=c1).count()}")
        self.stdout.write(f"  Enrollment  : {Enrollment.objects.filter(course=c1).count()}")
        self.stdout.write(f"  Assignment  : {Assignment.objects.filter(course=c1).count()}")
        self.stdout.write(f"  Submission  : {Submission.objects.filter(assignment=tugas).count()}")