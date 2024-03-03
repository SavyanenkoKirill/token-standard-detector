from django.http import HttpResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.core import serializers
from slither.slither import Slither

import json
from .models import Standard


@csrf_exempt
def verify_contract(request):
    body = json.loads(request.body)
    standard = Standard.objects.get(contract_address=body['contract_address'])
    standard_filename = f"{standard.contract_address}.sol"
    with open(standard_filename, "w") as file:
        file.write(standard.source_code)

    slither = Slither(standard_filename)
    contract = slither.get_contract_from_name('ERC20')
    # slither = Slither(standard_filename)
    return HttpResponse(contract[0].functions[0])
    # return HttpResponse(serializers.serialize('json', [standard]))
