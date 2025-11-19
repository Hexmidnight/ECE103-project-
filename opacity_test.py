from PIL import Image

def set_image_opacity(image_path, output_path, opacity_level):
    img = Image.open(image_path).convert('RGBA') 
    
    img.putalpha(opacity_level)
    
    img.save(output_path)
    print(f"Image saved with opacity {opacity_level} to {output_path}")

set_image_opacity('original_image.jpg', 'semi_transparent_image.png', 128)