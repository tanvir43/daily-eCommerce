import graphene

from graphene_django import DjangoObjectType, DjangoConnectionField

import graphene_django_optimizer as gql_optimizer

# from ..graphql.core.types.upload import Upload

from .models import Category

from graphene import relay, Node, Connection

# from graphene_django_optimizer.types import OptimizedDjangoObjectType

# from graphene_django.filter import DjangoFilterConnectionField

# from .utils.upload import Upload


class CategoryType(DjangoObjectType):
    class Meta:
        model = Category
        fields = ['id',
                  'name',
                  'slug',
                  'children',
                  'parent']
        interfaces = (relay.Node,)

    # def get_fields(self):
    #     fields = super(CategoryType, self).get_node(id=None, info=id)
    #     fields['children'] = CategoryType()
    #     return fields


class CategoryConnection(relay.Connection):
    class Meta:
        node = CategoryType

class Query(object):
    # category = relay.Node.Field(CategoryType)
    # ancestors = graphene.Field(
    #     lambda: graphene.List(CategoryType), description="List of ancestors of the category."
    # )
    # children = graphene.Field(
    #     lambda: graphene.List(CategoryType), description="List of children of the category."
    # )
    category = graphene.Field(lambda: graphene.List(CategoryType), id=graphene.ID())
    # category = graphene.Field(lambda: relay.ConnectionField(CategoryConnection), id=graphene.ID())
    # category = DjangoConnectionField(CategoryType, id=graphene.Int())
    # categories = graphene.List(CategoryType)
    categories = relay.ConnectionField(CategoryConnection)
    # categories = DjangoConnectionField(CategoryType)

    def resolve_category(self, info, **kwargs):
        pk = kwargs.get('id')
        if pk is not None:
            return Category.objects.get(pk=pk)

    def resolve_categories(self, info, **kwargs):
        print("Info", info)
        return gql_optimizer.query(Category.objects.all(), info)

    # @staticmethod
    # def resolve_ancestors(root: Category, info, **_kwargs):
    #     categories = Category.objects.all()
    #     qs = categories.get_ancestors()
    #     return gql_optimizer.query(qs, info)

    #@staticmethod
    # def resolve_children(root: Category, info, **_kwargs):
    #     qs = root.children.all()
    #     return gql_optimizer.query(qs, info)


class CategoryInput(graphene.InputObjectType):
    ID = graphene.ID
    name = graphene.String(description='Category name')
    slug = graphene.String(description='Category slug')
    # parent = graphene.ID(description="ID of the parent category. If empty, category will be top level category.",
    #                      name="parent")
    # background_image = Upload(description='Background image file')
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
