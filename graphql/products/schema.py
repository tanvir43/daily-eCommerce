import graphene
# from graphene import relay, Node, Connection
from graphene_django import DjangoObjectType, DjangoConnectionField

import graphene_django_optimizer as gql_optimizer
from graphene_django_optimizer.types import OptimizedDjangoObjectType

# from graphene_django.filter import DjangoFilterConnectionField
from ..core.types.upload import Upload

from products.models import Category


class CategoryType(DjangoObjectType):
    class Meta:
        model = Category
        # filter_fields = ['name']
        # interfaces = (relay.Node,)


class Query(object):
    # category = relay.Node.Field(CategoryType)

    category = graphene.Field(lambda: graphene.List(CategoryType), id=graphene.Int())
    # category = DjangoConnectionField(CategoryType, id=graphene.Int())
    categories = graphene.List(CategoryType)
    # categories = DjangoConnectionField(CategoryType)

    def resolve_category(root, info, **kwargs):
        pk = kwargs.get('id')
        if pk is not None:
            return gql_optimizer.query(Category.objects.get(pk=pk), info)

    def resolve_categories(root, info, **kwargs):
        return gql_optimizer.query(Category.objects.all(), info)


class CategoryInput(graphene.InputObjectType):
    ID = graphene.ID
    name = graphene.String(description='Category name')
    slug = graphene.String(description='Category slug')
    # parent = graphene.ID(description="ID of the parent category. If empty, category will be top level category.",
    #                      name="parent")
    background_image = Upload(description='Background image file')
    background_image_alt = graphene.String(description="Alt text for an image.")


class CreateCategory(graphene.Mutation):
    class Arguments:
        input = CategoryInput(
            required=True, description="Fields requred to create a category"
        )
        parent_id = graphene.ID(
            description=(
                "ID of the parent category. If empty, category will be top level "
                "category."
            ),
            name="parent",
        )
    category = graphene.Field(CategoryType)

    @staticmethod
    def mutate(root, info, input=None, **data):
        if 'parent_id' in data and data['parent_id']:
            parent_id = data['parent_id']
            parent_category = Category.objects.get(id=parent_id)
            category_instance = Category(name=input.name,
                                         slug = input.slug,
                                         parent = parent_category)
            category_instance.save()
            return CreateCategory(category=category_instance)
        else:
            category_instance = Category(name=input.name,
                                         slug=input.slug)
            category_instance.save()
            return CreateCategory(category=category_instance)


class Mutation(graphene.ObjectType):
    create_category = CreateCategory.Field()
    # update_actor = UpdateActor.Field()
    # create_movie = CreateMovie.Field()
    # update_movie = UpdateMovie.Field()
