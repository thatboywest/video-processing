from django import forms

class VideoUploadForm(forms.Form):
    video = forms.FileField(label='Select a video file')
    original_subtitles = forms.FileField(label='Select original subtitle file (SRT)')
    translated_subtitles = forms.FileField(label='Select translated subtitle file (SRT)')
    font = forms.FileField(label='Upload Font File', required=False)
    
    # Change overlay_color to use a color picker
    overlay_color = forms.CharField(
        label='Overlay Box Color',
        required=False,
        max_length=7,
        widget=forms.TextInput(attrs={'type': 'color'})
    )
    
    font_size = forms.IntegerField(label='Font Size', required=False, min_value=10, max_value=100)
    api_key = forms.CharField(label='Eleven Labs API Key', required=True, max_length=100)
    voice_id = forms.CharField(label='Eleven Labs Voice ID', required=True, max_length=50)
