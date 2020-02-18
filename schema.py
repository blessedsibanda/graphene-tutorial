import graphene
import json

class Query(graphene.ObjectType):
    hello = graphene.String()

    def resolve_hello(self, info):
        return 'world'

schema = graphene.Schema(query=Query)

result = schema.execute(
    '''
    {
        hello
    }
    '''
)

print(result.data.items())

print(result.data)
print(result.data['hello'])


# convert result to json
dictResult = dict(result.data.items())
json_result = json.dumps(dictResult, indent=2)

print(json_result)