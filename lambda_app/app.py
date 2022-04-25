# -*- coding: utf-8 -*-

from chalice import Chalice
from afwf_github.hdl import hello

app = Chalice(app_name="afwf_github")


@app.lambda_function(name="hello")
def handler_hello(event, context):
    return hello.high_level_api(event, context)
