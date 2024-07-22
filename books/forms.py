from django import forms
from django.core.validators import MinLengthValidator, MaxLengthValidator
from .widgets import CustomClearableFileInput
from .models import Book, Category, Review


class CategoryForm(forms.ModelForm):
    """ Form for creating and updating categories."""
    class Meta:
        model = Category
        fields = '__all__'

class BookForm(forms.ModelForm):
    """ Form for creating and updating books."""
    class Meta:
        model = Book
        exclude = ('discount', 'rating', 'add_to_wishlist', 'review_count',)

    image = forms.ImageField(label='Image', required=False, widget=CustomClearableFileInput)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        categories = Category.objects.all()
        friendly_names = [(c.id, c.get_friendly_name()) for c in categories]

        self.fields['category'].choices = friendly_names
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'border-black rounded-0'


class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['title', 'content', 'rating']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter title'}),
            'content': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Enter content'}),
            'rating': forms.NumberInput(attrs={'class': 'form-control', 'min': '1', 'max': '5'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['title'].validators.extend([
            MinLengthValidator(limit_value=2, message="Title must be at least 2 characters long."),
            MaxLengthValidator(limit_value=100, message="Title cannot exceed 100 characters.")
        ])
        self.fields['content'].validators.extend([
            MinLengthValidator(limit_value=10, message="Content must be at least 10 characters long."),
            MaxLengthValidator(limit_value=1000, message="Content cannot exceed 1000 characters.")
        ])

    def clean_rating(self):
        rating = self.cleaned_data.get('rating')
        if rating is None:
            raise forms.ValidationError("Rating is required.")
        if not (1 <= rating <= 5):
            raise forms.ValidationError("Rating must be between 1 and 5.")
        return rating