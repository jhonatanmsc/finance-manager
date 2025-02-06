from django import forms
from django.utils.safestring import mark_safe


class StarWidget(forms.RadioSelect):

    def stars(self, qtd):
        result = ""
        label_icon = '<i class=\"fa {icon}\" aria-hidden=\"true\"></i>'
        for i in range(qtd // 2):
            result += label_icon.format(icon='fa-star')
        if qtd % 2 != 0:
            result += label_icon.format(icon='fa-star-half-o')
        for i in range(10 - qtd // 2 if qtd > 0 else 0):
            result += label_icon.format(icon='fa-star-o')
        return result

    def render(self, name, value, attrs=None, renderer=None):
        html = super().render(name, value, attrs, renderer)
        # <i class="fa fa-star-half-o" aria-hidden="true"></i>
        # <i class="fa fa-star-o" aria-hidden="true"></i>
        stars_html = ''.join(
            "<div>"
            f'<label style="margin-right:5px;">'
            f'<input type="radio" name="{name}" value="{i}" {"checked" if str(i) == str(value) else ""}>' 
            f'{self.stars(i)}'
            f'</label>'
            '</div>'
            for i in range(1, 10)
        )
        return mark_safe(stars_html)