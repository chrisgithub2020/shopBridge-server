import os

def save_images(base64_image: list[str] | str, image_id: str):
    try:
        if not os.path.exists("./images"):
            os.mkdir("./images")

        with open(file=f"./images/{image_id}.ip", mode="w") as file: ## ip stands for item pic
            file.write(",".join(base64_image) if isinstance(base64_image, list) else base64_image)
    except Exception as err:
        print(err)
        return False

    return True

def load_image(image_id: str):
    try:
        with open(f"./images/{image_id}.ip", mode="r") as file:
            content = file.read()
            return content
    except Exception as err:
        print(err)
        return ""