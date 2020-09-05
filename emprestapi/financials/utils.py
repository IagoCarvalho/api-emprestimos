
def get_client_ip_address(request):
    http_x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    
    if http_x_forwarded_for:
        ip_address = http_x_forwarded_for.split(',')[-1].strip()
    else:
        ip_address = request.META.get('REMOTE_ADDR')
    return ip_address