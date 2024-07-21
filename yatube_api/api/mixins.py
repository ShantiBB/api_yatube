from rest_framework.viewsets import ModelViewSet


class AuthorPermissionMixin(ModelViewSet):
    def perform_create(self, serializer):
        self.perform_action(serializer=serializer, action='create')

    def perform_update(self, serializer):
        self.perform_action(serializer=serializer, action='update')

    def perform_destroy(self, instance):
        self.perform_action(instance=instance, action='destroy')
