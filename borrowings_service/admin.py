from django.contrib import admin

from borrowings_service.models import Borrowing, Payment

admin.site.register(Borrowing)
admin.site.register(Payment)
