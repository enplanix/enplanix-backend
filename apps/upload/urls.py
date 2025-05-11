from .views import FileUploadViewSet, ImageUploadViewSet

app_name = 'upload'

routes = [
    ('files', FileUploadViewSet, 'files'),
    ('images', ImageUploadViewSet, 'images'),
]