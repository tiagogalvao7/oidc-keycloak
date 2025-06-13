from django.shortcuts import render, redirect, get_object_or_404
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .forms import ClaimTableEducationForm, ClaimTableOSPForm, TransactionForm
from .models import ClaimTableEducation, ClaimTableOSP, Transaction
from .serializers import ClaimTableEducationSerializer, ClaimTableOSPSerializer, TransactionSerializer

# Existing views
def education_claim_list(request):
    claims = ClaimTableEducation.objects.all()
    return render(request, 'claims/education_claim_list.html', {'claims': claims})

def osp_claim_list(request):
    claims = ClaimTableOSP.objects.all()
    return render(request, 'claims/osp_claim_list.html', {'claims': claims})

def add_education_claim(request):
    if request.method == 'POST':
        form = ClaimTableEducationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('education_claim_list')  # Redirect to the list view after adding
    else:
        form = ClaimTableEducationForm()
    return render(request, 'claims/add_education_claim.html', {'form': form})

def add_osp_claim(request):
    if request.method == 'POST':
        form = ClaimTableOSPForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('osp_claim_list')  # Redirect to the list view after adding
    else:
        form = ClaimTableOSPForm()
    return render(request, 'claims/add_osp_claim.html', {'form': form})

# New JSON response view
@api_view(['GET'])
def get_claims_data(request, table_name):
    if table_name == 'education':
        model = ClaimTableEducation
        serializer = ClaimTableEducationSerializer
    elif table_name == 'osp':
        model = ClaimTableOSP
        serializer = ClaimTableOSPSerializer
    else:
        return Response({'error': 'Invalid table name'}, status=400)

    claim_designation = request.GET.get('claim_designation')

    if claim_designation:
        claim = get_object_or_404(model, claim_designation=claim_designation)
        data = serializer(claim).data
        return Response(data)
    else:
        claims = model.objects.all()
        data = serializer(claims, many=True).data
        return Response(data)

# List transactions
def transaction_list(request):
    transactions = Transaction.objects.all()
    return render(request, 'transactions/transaction_list.html', {'transactions': transactions})

# Add a new transaction
def add_transaction(request):
    if request.method == 'POST':
        form = TransactionForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('transaction_list')  # Redirect to the list view after adding
    else:
        form = TransactionForm()
    return render(request, 'transactions/add_transaction.html', {'form': form})

# New view to add a transaction via Flask API
@api_view(['POST'])
def add_transaction_api(request):
    """
    Add a new transaction received from Flask API.
    """
    serializer = TransactionSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response({'message': 'Transaction added successfully'}, status=201)
    else:
        return Response({'error': 'Invalid data'}, status=400)

@api_view(['PUT'])
def update_transaction_api(request, pk):
    """
    Update an existing transaction received from the Flask API.
    """
    try:
        transaction = Transaction.objects.get(name=name)  # Avoid using get_object_or_404 to handle manually
        data = TransactionSerializer(transaction).data
        return Response(data)
    except Transaction.DoesNotExist:
        # If the transaction does not exist, return a 404 response without throwing an internal error
        return Response({'error': f'Transaction with name "{name}" not found.'}, status=404)
    except Exception as e:
        return Response({'error': str(e)}, status=500)

# New view to get a specific transaction by name via Flask API
@api_view(['GET'])
def get_transaction_api(request, name):
    """
    Get a specific transaction by name received from Flask API.
    """
    try:
        transaction = Transaction.objects.get(name=name)  # Avoid using get_object_or_404 to handle manually
        data = TransactionSerializer(transaction).data
        return Response(data)
    except Transaction.DoesNotExist:
        # If the transaction does not exist, return a 404 response without throwing an internal error
        return Response({'error': f'Transaction with name "{name}" not found.'}, status=404)
    except Exception as e:
        # Catch any other general errors and return 500 with details
        return Response({'error': f'Unexpected error: {str(e)}'}, status=500)