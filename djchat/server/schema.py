from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import OpenApiParameter, extend_schema

from .serializer import ChannelSerializer, ServerSerializer

server_list_docs = extend_schema(
    responses=ServerSerializer(many=True),
    parameters=[
        OpenApiParameter(
            name="category",
            type=OpenApiTypes.STR,
            location=OpenApiParameter.QUERY,
            description="Category of server to retrive",
        ),
        OpenApiParameter(
            name="qty",
            type=OpenApiTypes.INT,
            location=OpenApiParameter.QUERY,
            description="Number of server to retrive",
        ),
        OpenApiParameter(
            name="by_user",
            type=OpenApiTypes.BOOL,
            location=OpenApiParameter.QUERY,
            description="filter server by the  current authenticated user (true/false)",
        ),
        OpenApiParameter(
            name="with_num_members",
            type=OpenApiTypes.BOOL,
            location=OpenApiParameter.QUERY,
            description="Include the no of member of each data set",
        ),
        OpenApiParameter(
            name="by_serverid",
            type=OpenApiTypes.INT,
            location=OpenApiParameter.QUERY,
            description="Include server by id",
        ),
    ],
)
