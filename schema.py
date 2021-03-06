import graphene
import json
from datetime import datetime
import uuid

class Post(graphene.ObjectType):
    title = graphene.String()
    content = graphene.String()

class User(graphene.ObjectType):
    id = graphene.ID(default_value=str(uuid.uuid4()))
    username = graphene.String()
    created_at = graphene.DateTime(default_value=datetime.now())

    avatar_url = graphene.String()
    def resolve_avatar_url(self, info):
        return 'https://cloudinary.com/{}/{}'.format(self.username,
            self.id)

class Query(graphene.ObjectType):
    hello = graphene.String()
    is_admin = graphene.Boolean()
    users = graphene.List(User, limit=graphene.Int())

    def resolve_hello(self, info):
        return 'world'

    def resolve_is_admin(self, info):
        return True 

    def resolve_users(self, info, limit=None):
        return [
            User(id="1", username="Fred", created_at=datetime.now()),
            User(id="2", username="Jane", created_at=datetime.now()),
            User(id="3", username="Samantha", created_at=datetime.now()),
            User(id="4", username="Blessed", created_at=datetime.now()),
        ][:limit]

class CreateUser(graphene.Mutation):
    user = graphene.Field(User)

    class Arguments:
        username = graphene.String()

    def mutate(self, info, username):
        user = User(username=username)
        return CreateUser(user=user)

class CreatePost(graphene.Mutation):
    post = graphene.Field(Post)

    class Arguments:
        title = graphene.String()
        content = graphene.String()

    def mutate(self, info, title, content):
        if info.context.get('is_anonymous'):
            raise Exception('Not authenticated!')
        post = Post(title=title, content=content)
        return CreatePost(post=post)

class Mutation(graphene.ObjectType):
    create_user = CreateUser.Field()
    create_post = CreatePost.Field()

schema = graphene.Schema(query=Query, mutation=Mutation)

result = schema.execute(
    '''
    {
        users {
            id
            createdAt
            username
            avatarUrl
        }
    }
    ''',
    # variable_values={'limit': 3}
    # context={'is_anonymous': True}
)

print(result.errors)
# print(result.data.items())

print(result.data)

# convert result to json
dictResult = dict(result.data.items())
json_result = json.dumps(dictResult, indent=2)

print(json_result)