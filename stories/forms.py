from django import forms
from stories.models import Story


class NewStoryForm(forms.ModelForm):
	# content = forms.FileField(widget=forms.ClearableFileInput(attrs={'multiple': True}), required=True)
	caption = forms.CharField(widget=forms.Textarea(attrs={'class': 'input is-medium'}), required=False)

	class Meta:
		model = Story
		fields = ('content', 'caption')