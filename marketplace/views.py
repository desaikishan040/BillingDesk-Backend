from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view, action
from rest_framework.views import APIView
from .serializer import ProposalSerializer,ProposalAllSerializer
from rest_framework.decorators import permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from .models import Proposal


@permission_classes([IsAuthenticated])
class RequireItem(APIView):
    def get(self, request, *args, **kwargs):
        data = Proposal.objects.filter(user=request.user).order_by('-created_on')
        serializeddata = ProposalAllSerializer(data, many=True)
        return Response({"status": "success", "data": serializeddata.data}, status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        request.data['user'] = request.user.id
        serializer = ProposalSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"status": "success", "data": serializer.data}, status=status.HTTP_200_OK)
        else:
            return Response({"status": "error", "data": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def RequireItemAll(request):
    data = Proposal.objects.all().exclude(user=request.user).order_by('-created_on')
    serializeddata = ProposalAllSerializer(data, many=True)
    return Response({"status": "success", "data": serializeddata.data}, status.HTTP_200_OK)
