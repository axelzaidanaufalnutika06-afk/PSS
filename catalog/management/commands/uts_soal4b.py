"""UTS PSS - Soal 4b: tampilkan hasil 6 query ORM.
Jalankan (setelah uts_soal4a): docker compose exec app python manage.py uts_soal4b
"""
from django.core.management.base import BaseCommand

from catalog.models import Assignment, Course, Enrollment, Lesson, Submission
from users.models import User


class Command(BaseCommand):
    help = "Soal 4b: 6 query ORM"

    def handle(self, *args, **options):
        dosen = User.objects.get(username="suprayogi")
        course = Course.objects.get(code="PSS01")
        tugas = Assignment.objects.get(course=course, title="Tugas Django ORM")
        w = self.stdout.write

        w("1. Semua Course beserta kode dan judulnya")
        for c in Course.objects.filter(code__in=["PSS01", "BD01"]):
            w(f"   {c.code} - {c.title}")

        w(f"2. Course yang diampu {dosen.username}")
        for c in Course.objects.filter(lecturer=dosen, code__in=["PSS01", "BD01"]):
            w(f"   {c.code} - {c.title}")

        w(f"3. Semua Lesson milik {course.code}")
        for l in Lesson.objects.filter(course=course).order_by("order"):
            w(f"   {l.order}. {l.title}")

        w(f"4. Jumlah mahasiswa terdaftar di {course.code}: "
          f"{Enrollment.objects.filter(course=course).count()}")

        w(f"5. Semua Assignment milik {course.code}")
        for a in Assignment.objects.filter(course=course):
            w(f"   {a.title} (deadline {a.deadline:%Y-%m-%d})")

        w(f"6. Semua Submission milik '{tugas.title}'")
        for s in Submission.objects.filter(assignment=tugas).select_related("student"):
            w(f"   {s.student.username} | nilai {s.grade}")