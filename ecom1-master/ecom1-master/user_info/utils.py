def get_client_ip_address(request):
    x_forwarded=request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded:
        ip=x_forwarded.split(",")[0]
    else:
        ip=request.META.get('REMOTE_ADDR',None)


    return ip
