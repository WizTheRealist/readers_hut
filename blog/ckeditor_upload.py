from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.admin.views.decorators import staff_member_required
import cloudinary.uploader
import os

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

    # In blog/ckeditor_upload.py
@staff_member_required
def debug_cloudinary(request):
    config = cloudinary.config()
    return JsonResponse({
        'cloud_name': config.cloud_name,
        'api_key': config.api_key[:5] + '***' if config.api_key else None,
        'api_secret': '***' if config.api_secret else None,
        'env_cloud_name': os.getenv("CLOUDINARY_CLOUD_NAME"),
        'env_api_key': os.getenv("CLOUDINARY_API_KEY")[:5] + '***' if os.getenv("CLOUDINARY_API_KEY") else None,
    })