import graphene
import json
from datetime import datetime

class User(graphene.ObjectType):
    id = graphene.ID()
    username = graphene.String()
    created_at = graphene.DateTime()

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
        user = User(id="3",username=username, 
            created_at=datetime.now())
        return CreateUser(user=user)

class Mutation(graphene.ObjectType):
    create_user = CreateUser.Field()

schema = graphene.Schema(query=Query, mutation=Mutation)

result = schema.execute(
    '''
    mutation {
        createUser(username: "Jeff") {
            user {
                id
                username
                createdAt
            }
        }
    }
    '''
)

print(result.errors)
# print(result.data.items())

print(result.data)

# convert result to json
dictResult = dict(result.data.items())
json_result = json.dumps(dictResult, indent=2)

print(json_result)