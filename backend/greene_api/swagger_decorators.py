from drf_yasg import openapi


param_query_hint = openapi.Parameter(
    'query',
    openapi.IN_QUERY,
    description='A sting that be filtered on list of posts',
    type=openapi.TYPE_STRING
)
