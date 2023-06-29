from django.db.models import Count
from rest_framework import viewsets
from rest_framework.exceptions import AuthenticationFailed, ValidationError
from rest_framework.response import Response

from .models import Server
from .schema import server_list_docs
from .serializer import ServerSerializer


class ServiceListViewSet(viewsets.ViewSet):
    queryset = Server.objects.all()

    @server_list_docs
    def list(self, request):
        """Fetches a list of servers based on the provided query parameters.

        Args:
            request (Request): The HTTP request object containing the query parameters.

        Returns:
            Response: The HTTP response containing the serialized server data.

        Raises:
            AuthenticationFailed: If the 'by_user' parameter is set to true but the user is not authenticated.
            ValidationError: If there is an error with the query parameter values.

        Query Parameters:
            - category (str): Optional. Filters the servers by the specified category name.
            - qty (int): Optional. Limits the number of servers to be returned.
            - by_user (bool): Optional. If set to true, filters the servers by the currently authenticated user.
            - by_serverid (str): Optional. Filters the servers by the specified server ID.
            - with_num_members (bool): Optional. If set to true, includes the number of members for each server.

        Note:
            - The 'by_user' parameter requires the user to be authenticated. Otherwise, an AuthenticationFailed exception is raised.
            - The 'by_serverid' parameter should be a valid server ID. If the server with the specified ID is not found, a ValidationError is raised.
            - The 'with_num_members' parameter, when set to true, adds an additional 'num_members' field to each serialized server object.

        """

        # Extract query parameters from the request
        category = request.query_params.get("category")
        qty = request.query_params.get("qty")
        by_user = request.query_params.get("by_user") == "true"
        by_serverid = request.query_params.get("by_serverid")
        with_num_members = request.query_params.get("with_num_members") == "true"

        # Filter queryset based on category, if provided
        if category:
            self.queryset = self.queryset.filter(category__name=category)

        # Filter queryset based on the authenticated user, if requested
        if by_user and request.user.is_authenticated:
            user_id = request.user.id
            self.queryset = self.queryset.filter(member=user_id)
        else:
            raise AuthenticationFailed()

        # Annotate queryset with the number of members, if requested
        if with_num_members:
            self.queryset = self.queryset.annotate(num_members=Count("member"))

        # Limit the queryset to a specific quantity, if provided
        if qty:
            self.queryset = self.queryset[: int(qty)]

        # Filter queryset based on server ID, if provided
        if by_serverid:
            if not request.user.is_authenticated:
                raise AuthenticationFailed()
            try:
                self.queryset = self.queryset.filter(id=by_serverid)
                if not self.queryset.exists():
                    raise ValidationError(detail=f"Server with id {by_serverid} not found")
            except ValueError:
                raise ValidationError(detail="Server value error")

        # Serialize the queryset using the ServerSerializer
        serializer = ServerSerializer(self.queryset, many=True, context={"num_members": with_num_members})

        # Return the serialized data as a response
        return Response(serializer.data)
