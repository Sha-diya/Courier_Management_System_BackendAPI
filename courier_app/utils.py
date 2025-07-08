from rest_framework.views import exception_handler
from rest_framework.response import Response
from rest_framework import status


def success_response(data=None, message="Success", status_code=200):
    return Response({
        "success": True,
        "statusCode": status_code,
        "message": message,
        "Data": data or {}
    }, status=status_code)

def error_response(errors=None, message="Something went wrong", status_code=400):
    return Response({
        "success": False,
        "statusCode": status_code,
        "message": message,
        "Data": errors or {}
    }, status=status_code)

def custom_exception_handler(exc, context):
    response = exception_handler(exc, context)

    if response is not None:
        return Response({
            'success': False,
            'statusCode': response.status_code,
            'message': str(exc),
            'Data': {}
        }, status=response.status_code)

    return Response({
        'success': False,
        'statusCode': 500,
        'message': 'Internal server error',
        'Data': {}
    }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
