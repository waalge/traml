import traml 

if __name__ == "__main__":
    request_ids = [4627, 4439, 120, 99, 100, 119, 135, 136, 3516]
    result = traml.get_wiener_linien_data.wl_data(request_ids[0])
    print(result)
