from rest_framework.generics import GenericAPIView
from rest_framework import status, filters
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from protocol.models import SkillTag
from protocol.serializers import SkillTagSerializer

class SkillTagView(GenericAPIView):

    queryset = SkillTag.objects.all()
    serializer_class = SkillTagSerializer
    filter_backends = [filters.SearchFilter]
    search_field = ['name']

    def get(self, request):

        skill_tag = self.filter_queryset(self.get_queryset())[:10]

        # search = request.query_params.get('search', '')

        # if not search:
        #     skill_tag = self.get_queryset()[:10]
        # else:
        #     skill_tag = self.get_queryset().filter(name__icontains=search)[:10]
        
        serializer = self.get_serializer(skill_tag, many=True)

        return Response(
            status = status.HTTP_200_OK,
            data = serializer.data,
        )

    def post(self, request):
        serializer = self.get_serializer(request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(
            status=status.HTTP_201_CREATED,
            data = serializer.data,
        )

    def delete(self, request, uuid):
        skill_tag = get_object_or_404(self.get_queryset(), uuid=uuid)
        skill_tag.delete()

        return Response(
            status = status.HTTP_204_NO_CONTENT,
        )