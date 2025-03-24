from django.contrib import admin


class CustomModelAdmin(admin.ModelAdmin):

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(users=request.user)

    def save_model(self, request, obj, form, change):
        if not change:
            obj.users.add(request.user)
        super().save_model(request, obj, form, change)