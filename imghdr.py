def what(file, h=None):
    if h is None:
        try:
            with open(file, 'rb') as f:
                h = f.read(32)
        except Exception:
            return 'png'
    
    if h.startswith(b'\x89PNG\r\n\x1a\n'):
        return 'png'
    elif h.startswith(b'\xff\xd8'):
        return 'jpeg'
    elif h.startswith(b'GIF87a') or h.startswith(b'GIF89a'):
        return 'gif'
        
    return 'png'
