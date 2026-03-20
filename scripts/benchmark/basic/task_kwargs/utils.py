def image2base64(file_path):
    import base64
    from PIL import Image

    with Image.open(file_path) as img:
        # PIL会在打开时验证是否为有效图像
        img_format = (img.format or "").lower()
        mime_type = "application/octet-stream"
        if img_format in (".jpg", ".jpeg"): mime_type = "image/jpeg"
        if img_format in (".png",): mime_type = "image/png"
        if img_format in (".webp",): mime_type = "image/webp"
        if img_format in (".bmp",): mime_type = "image/bmp"
        if img_format in (".tif", ".tiff"): mime_type = "image/tiff"

    with open(file_path, "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read()).decode("utf-8")
    return f"data:{mime_type};base64,{encoded_string}"