from rest_framework.response import Response


def send_jwt_error_response(msg):
    return Response({"success": False, "message": msg})
