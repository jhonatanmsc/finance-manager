from django import forms

from goals.admin_widgets import StarWidget
from goals.models import Supplier


class SupplierForm(forms.ModelForm):
    class Meta:
        model = Supplier
        fields = '__all__'
        widgets = {
            'rating': StarWidget(),
        }

    class Media:
        css = {
            'all': (
                'https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.7.2/css/all.min.css',
                'css/custom-admin.css',
            ),
            'js': (
                'js/custom-admin.js'
            )
        }