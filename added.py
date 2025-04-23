with open("Bike_upscaled_max_quality.jpg", "rb") as f1, open("Bike_upscaled_max_quality_copy.jpg", "wb") as f2:
    f2.write(f1.read())
    f2.write(b"\0" * 500000)