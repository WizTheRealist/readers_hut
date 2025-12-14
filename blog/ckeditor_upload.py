from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.admin.views.decorators import staff_member_required
import cloudinary.uploader

@staff_member_required
@csrf_exempt
def upload_image(request):
    if request.method == 'POST' and request.FILES.get('upload'):
        file = request.FILES['upload']
        
        try:
            # Upload to Cloudinary with explicit options
            result = cloudinary.uploader.upload(
                file,
                folder="ckeditor_uploads",
                resource_type="auto",
                allowed_formats=['jpg', 'jpeg', 'png', 'gif', 'webp']
            )
            
            return JsonResponse({
                'url': result['secure_url'],
                'uploaded': 1
            })
        except Exception as e:
            return JsonResponse({
                'uploaded': 0,
                'error': {
                    'message': str(e)
                }
            })
    
    return JsonResponse({'uploaded': 0, 'error': {'message': 'No file uploaded'}})