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
    users = graphene.List(User)

    def resolve_hello(self, info):
        return 'world'

    def resolve_is_admin(self, info):
        return True 

    def resolve_users(self, info):
        return [
            User(id="1", username="Fred", created_at=datetime.now()),
            User(id="2", username="Jane", created_at=datetime.now()),
            User(id="3", username="Samantha", created_at=datetime.now()),
            User(id="4", username="Blessed", created_at=datetime.now()),
        ]

schema = graphene.Schema(query=Query, auto_camelcase=False)

result = schema.execute(
    '''
    {
        users {
            username
            id
            created_at
        }
    }
    '''
)

print(result.data.items())

print(result.data)

# convert result to json
dictResult = dict(result.data.items())
json_result = json.dumps(dictResult, indent=2)

print(json_result)