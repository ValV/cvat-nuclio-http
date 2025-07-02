# This source is a modification of CVAT SAM 'main.py'
#
# Copyright (C) 2023 CVAT.ai Corporation
#
# SPDX-License-Identifier: MIT
#
# See https://github.com/ValV/cvat-nuclio-http

# import base64
import json

from os import getenv
from urllib.request import Request, urlopen


SAM_URI = "http://host.docker.internal:51515/features"


def init_context(context):
    context.logger.info("Init context...  0%")
    # model = ModelHandler()
    # context.user_data.model = model
    # context.logger.info("Init context... 50%")
    context.user_data.sam_uri = getenv("SAM_URI", SAM_URI)
    context.logger.debug("URL = %s", context.user_data.sam_uri)
    context.logger.info("Init context...100%")


def handler(context, event):
    context.logger.info("Call handler")
    data = event.body
    # buf = io.BytesIO(base64.b64decode(data["image"]))
    # image = Image.open(buf)
    # image = image.convert("RGB")  #  to make sure image comes in RGB
    # features = context.user_data.model.handle(image)

    url = context.user_data.sam_uri
    context.logger.debug("URL = %s", url)
    request = Request(url, data=json.dumps(data).encode("utf-8"), method="POST")
    for key, value in dict(event.headers).items():
        request.add_header(key, value)
    try:
        with urlopen(request) as response:
            data_response = response.read()  # bytes
            context.logger.info(
                "Response from SAM service: size = %d bytes, type is %s",
                len(data_response),
                str(type(data_response)),
            )
            # context.logger.info("Response headers: %s", response.info())
            result = data_response.decode("utf-8")  # string

            # Return the response back to the original caller
            return context.Response(
                body=result,
                # body = json.dumps({
                #     'blob': base64.b64encode((features.cpu().numpy() if features.is_cuda else features.numpy())).decode(),
                # }),
                headers={},  # TODO: forward headers
                content_type="application/json",
                status_code=200,
            )
    except Exception as e:
        context.logger.error("Error forwarding request: %s", str(e))
        return context.Response(body=json.dumps({"Error": str(e)}), status_code=500)
