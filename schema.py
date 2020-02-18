import graphene
import json

class Query(graphene.ObjectType):
    hello = graphene.String()
    is_admin = graphene.Boolean()

    def resolve_hello(self, info):
        return 'world'

    def resolve_is_admin(self, info):
        return True 

schema = graphene.Schema(query=Query, auto_camelcase=False)

result = schema.execute(
    '''
    {
        is_admin
    }
    '''
)

print(result.data.items())

print(result.data)

# convert result to json
dictResult = dict(result.data.items())
json_result = json.dumps(dictResult, indent=2)

print(json_result)