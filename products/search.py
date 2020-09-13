#products/search.py

from elasticsearch_dsl.query import Q, MultiMatch, SF
from .documents.product import ProductDoc


def get_search_query(phrase):
    # query = Q(
    #     'function_score',
    #     query=MultiMatch(
    #         fields=['name', 'slug', 'description', 'count_sold'],
    #         query=phrase
    #     ),
    #     functions=[
    #         SF('field_value_factor', field='count_sold')
    #     ]
    # )
    query = MultiMatch(query=phrase, fields=['name'],
                        fuzziness='AUTO')
    # return ProductDocument.search().query('match', name=phrase)
    return ProductDocument.search().query(query)


def search(phrase):
    return get_search_query(phrase).to_queryset()

# def search(phrase):
#     return ProductDocument.search().query(phrase)