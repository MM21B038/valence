from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from dnd.models import AppTheme
from dnd.serializers import AppThemeSerializer

def set_default_to_false():
    app_theme_default = AppTheme.objects.filter(default=True)
    if app_theme_default.exists():
        app_theme_default.update(default=False)

class AppThemeView(GenericAPIView):

    queryset = AppTheme.objects.all()
    serializer_class = AppThemeSerializer

    def get(self, request):

        app_theme = self.get_queryset()
        serializer = self.get_serializer(app_theme, many=True)

        return Response(
            status = status.HTTP_200_OK,
            data = serializer.data,
        )

    def post(self, request):

        set_default_to_false()
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(
            status = status.HTTP_201_CREATED,
            data = serializer.data,
        )

    def patch(self, request, uuid):

        set_default_to_false()

        app_theme = get_object_or_404(self.get_queryset(), uuid=uuid)
        serializer = self.get_serializer(app_theme, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        app_theme = serializer.save()
        app_theme.default = True
        app_theme.save()

        return Response(
            status = status.HTTP_200_OK,
            data = self.get_serializer(app_theme).data,
        )

    def delete(self, request, uuid):
        app_theme = get_object_or_404(self.get_queryset(), uuid=uuid)
        app_theme.delete()

        return Response(
            status = status.HTTP_204_NO_CONTENT,
        )





