from django import forms

class VideoUploadForm(forms.Form):
    video = forms.FileField(label='Select a video file')
    subtitles = forms.FileField(label='Select a subtitle file (SRT)')
    font = forms.FileField(label='Upload Font File', required=False)
    overlay_color = forms.CharField(label='Overlay Box Color (Hex Code)', required=False, max_length=7)
    font_size = forms.IntegerField(label='Font Size', required=False, min_value=10, max_value=100)
