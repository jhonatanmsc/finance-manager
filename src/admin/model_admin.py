from django.contrib import admin


class CustomModelAdmin(admin.ModelAdmin):

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(users=request.user)

    def save_related(self, request, form, formset, change):
        super().save_related(request, form, formset, change)
        if not change:
            form.instance.users.add(request.user)
