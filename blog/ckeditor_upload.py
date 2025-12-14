from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.admin.views.decorators import staff_member_required
import cloudinary.uploader
import os
import logging

logger = logging.getLogger(__name__)

@staff_member_required
@csrf_exempt
def upload_image(request):
    if request.method == 'POST' and request.FILES.get('upload'):
        file = request.FILES['upload']
        
        # Log file details
        logger.error(f"File name: {file.name}")
        logger.error(f"File size: {file.size}")
        logger.error(f"Content type: {file.content_type}")
        logger.error(f"File object type: {type(file)}")
        
        try:
            # Read file content
            file_content = file.read()
            logger.error(f"File content length: {len(file_content)}")
            logger.error(f"First 20 bytes: {file_content[:20]}")
            
            # Reset file pointer
            file.seek(0)
            
            # Upload directly to Cloudinary with the file object
            result = cloudinary.uploader.upload(
                file,
                folder="blog_images",
                resource_type="image",
            )
            
            return JsonResponse({
                'url': result['secure_url'],
                'uploaded': 1
            })
        except Exception as e:
            logger.error(f"Upload error: {str(e)}")
            return JsonResponse({
                'uploaded': 0,
                'error': {
                    'message': f'Upload failed: {str(e)}'
                }
            })
    
    return JsonResponse({
        'uploaded': 0, 
        'error': {'message': 'No file uploaded'}
    })

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