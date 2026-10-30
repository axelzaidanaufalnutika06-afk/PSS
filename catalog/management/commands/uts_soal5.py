"""UTS PSS - Soal 5: eksperimen optimasi query.
Prasyarat (sekali saja):
  docker compose exec app python manage.py generate_performance_data
  docker compose exec app python manage.py generate_relationship_data
Jalankan: docker compose exec app python manage.py uts_soal5
"""
from django.core.management.base import BaseCommand
from django.db import connection
from django.test.utils import CaptureQueriesContext

from catalog.models import Course

N = 100  # jumlah Course yang diuji (ubah bila perlu, catat di laporan)


def hitung(fn):
    with CaptureQueriesContext(connection) as ctx:
        fn()
    return len(ctx)


class Command(BaseCommand):
    help = "Soal 5: bandingkan jumlah query sebelum/sesudah optimasi"

    def handle(self, *args, **options):
        ids = list(Course.objects.filter(code__startswith="PERF")
                   .order_by("code").values_list("id", flat=True)[:N])
        self.stdout.write(f"Jumlah Course PERF di DB : "
                          f"{Course.objects.filter(code__startswith='PERF').count()}")
        self.stdout.write(f"Jumlah data diuji (N)    : {len(ids)}\n")

        # 5a. Tanpa select_related -> N+1
        def tanpa():
            for c in Course.objects.filter(id__in=ids):
                _ = c.lecturer.username
        a = hitung(tanpa)

        # 5b. Dengan select_related -> JOIN
        def dengan():
            for c in Course.objects.filter(id__in=ids).select_related("lecturer"):
                _ = c.lecturer.username
        b = hitung(dengan)

        # 5c. Course + Lesson
        def lesson_tanpa():
            for c in Course.objects.filter(id__in=ids):
                _ = [l.title for l in c.lessons.all()]
        c_before = hitung(lesson_tanpa)

        def lesson_prefetch():
            for c in Course.objects.filter(id__in=ids).prefetch_related("lessons"):
                _ = [l.title for l in c.lessons.all()]
        c_after = hitung(lesson_prefetch)

        self.stdout.write("=== TABEL HASIL ===")
        self.stdout.write(f"{'Skenario':<20}{'Jumlah Data':<14}{'Sebelum':<10}{'Sesudah':<10}")
        self.stdout.write(f"{'Course + Lecturer':<20}{len(ids):<14}{a:<10}{b:<10}")
        self.stdout.write(f"{'Course + Lesson':<20}{len(ids):<14}{c_before:<10}{c_after:<10}")

        # 5d. EXPLAIN
        self.stdout.write("\n=== EXPLAIN: filter code (kolom unique/ber-index) ===")
        self.stdout.write(Course.objects.filter(code="PERF00010").explain())
        self.stdout.write("\n=== EXPLAIN: filter description (tanpa index) ===")
        self.stdout.write(Course.objects.filter(description="xyz").explain())
        self.stdout.write("\n=== EXPLAIN: filter is_active=True (80% baris) ===")
        self.stdout.write(Course.objects.filter(is_active=True).explain())