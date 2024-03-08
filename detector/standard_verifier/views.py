import json
import os

from django.http import HttpResponse, Http404
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.core import serializers
from slither.slither import Slither
from .erc20.erc20 import get_visible_functions
from .erc20.erc20 import verify_signatures
from .erc20.constants import ERC20_FX_SIGNATURES, ERC20_LATEST_VERSION
from .models import Standard
from slither.exceptions import SlitherError


@csrf_exempt
def verify_contract(request):
    body = json.loads(request.body)
    try:
        standard = Standard.objects.get(contract_address=body['contract_address'])
    except Standard.DoesNotExist:
        raise Http404
    standard.status = 'PROCESSING'
    standard.save()
    standard_token_type = standard.token_type
    standard_filename = f'{standard.contract_address}.sol'
    with open(standard_filename, 'w') as file:
        file.write(standard.source_code)
    try:
        slither = Slither(standard_filename)
        contracts = slither.get_contract_from_name(standard_token_type)
        os.remove(standard_filename)
        standard.is_correct = True
        if len(contracts) == 0:
            standard.is_correct = False
            standard.status = 'COMPLETED'
            standard.save()
            return HttpResponse(
                f"Contract {body['contract_address']} Is Not {standard_token_type}",
                status=200
            )
        standard.version = ERC20_LATEST_VERSION
        # output signatures extra info
        contract = contracts[0]
        visible_functions = get_visible_functions(contract.functions)
        erc20_fx_matches = verify_signatures(visible_functions, ERC20_FX_SIGNATURES)
        signature_matches = {
            match[0].to_string(True): match[1] is not None for match in erc20_fx_matches
        }
        standard.status = 'COMPLETED'
        standard.save()
        return HttpResponse(json.dumps(signature_matches), status=200)
    except SlitherError as e:
        standard.status = 'FAILED'
        standard.is_correct = False
        standard.save()
        return HttpResponse({'error': str(e)}, status=500)

    # return HttpResponse(serializers.serialize('json', [standard]))
