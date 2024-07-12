from django import forms
from .widgets import CustomClearableFileInput
from .models import Book, Category


class CategoryForm(forms.ModelForm):
    """ Form for creating and updating categories."""
    class Meta:
        model = Category
        fields = '__all__'

class BookForm(forms.ModelForm):
    """ Form for creating and updating books."""
    class Meta:
        model = Book
        exclude = ('discount', 'rating', 'add_to_whishlist', 'review_count',)

    image = forms.ImageField(label='Image', required=False, widget=CustomClearableFileInput)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        categories = Category.objects.all()
        friendly_names = [(c.id, c.get_friendly_name()) for c in categories]

        self.fields['category'].choices = friendly_names
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'border-black rounded-0'