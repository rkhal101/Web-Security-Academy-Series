# REST API & GraphQL
**General info and vulnerabilities**

**For reference The Uniform Resource Locator, (URL):**


![URI](https://github.com/LinuxUser255/Web-Security-Academy-Series/assets/46334926/77ac059e-2e7d-48bd-80b7-c979a9f2f11f)




a URL is a reference to a resource that specifies its location on a computer network and a mechanism for retrieving,
and is  a specific type of URI

And the Uniform Resource Identifier (URI) is a compact sequence of characters that identifies an abstract or physical resource.

Another illustration:
- `Protocol://hostname[:portNumber]/[path]/[?query][params]`

### REST API URL Structure
- `https://example.com/api/v3/users`
- `https://example.com/api/v3/customers`
- `https://example.com/api/v3/updated_on`
- `https://example.com/api/v3/state/1/`


## API Resources explained
- **Singleton: resource that is a unique object**
  `/api/profiles/{user_id}`

- **Collection is a group of resources**
 `/api/profiles/users`

- **Sub-collection refers to a collection within a particular resource**
 `/api/profiles/{user_id}/settings`


### REST API Hacking Tools
- https://github.com/assetnote/kiterunner
- https://github.com/owasp-amass/amass
- https://github.com/sullo/nikto



# GraphQL
GraphQL is an API query language that is designed to facilitate efficient communication between clients and servers. It enables the user to specify exactly what data they want in the response, helping to avoid the large response objects and multiple calls that can sometimes be seen with REST APIs.


## The GraphQL query process
1. Client sends a POST request to the server
2. Server processes the query via the Query Parser
3. Query Parser validates the query's formatting
4. Resolver Functions generate response for a valid query


The **Query Parser** is responsible for turning the query string into an
**_Abstract Syntax Tree_ (AST)**
Then validating the query string against the schema to ensure that only 
valid queries are accepted.

**Resolver Functions**  populate the response with data for each specified field in the client query. This is done by implementing code logic which queries Relational DBs, Cache DBs, or other Servers on the network.
Each field has a corresponding resolver function that returns the field's response.

**Because resolver functions are the GraphQL component responsible for resolving queries, this is also where  vulnerabilities can exist**
It is common for GraphQL APIs to make calls to REST APIs

### REST API vs GraphQL
Use GQL when you need an efficient way to query multiple fields/data, or to customize and select just a few.
With REST API, you must query two or more endpoints, and cannot customize how
much data is returned. GraphQL solves the problem of under-fetching and over-fetching.
For example, looking up info on some web app users as an admin:
- `/rest/v1/users`
- `/rest/v1/history/1`

![API_RESTvsGraphQL](https://github.com/LinuxUser255/Web-Security-Academy-Series/assets/46334926/ffedc3fe-dd30-4b4b-b746-7ba46f31dd96)

<br>

To avoid over-fetching, you can modify the GQL request to only retrieve certain data. So if you only wanted to know the user's id, email and last name, then just edit your query.

![Screenshot_20240410_164143](https://github.com/LinuxUser255/Web-Security-Academy-Series/assets/46334926/87f96ced-d0e7-42e6-92c1-d6108deecc7f)



### Introspection Queries

- An Introspection Query is a feature in GraphQL that allows it to describe it's own data to the client. 

- Schemas represent the structure of the app's data model. 
- And, In order to interact with a GQL API devs need to know: 
- the data that can be accessed & 
- what queries or mutations the API supports. 

### GraphQL exposes this schema information via the Introspection Query
### Request:
```GraphQL
query IntrospectionQuery {
  __schema {
    queryType {
      name
    }
    mutationType {
      name
    }
    subscriptionType {
      name
    }
    types {
      ...FullType
    }
    directives {
      name
      description
      locations
      args {
        ...InputValue
      }
    }
  }
}
fragment FullType on __Type {
  kind
  name
  description
  fields(includeDeprecated: true) {
    name
    description
    args {
      ...InputValue
    }
    type {
      ...TypeRef
    }
    isDeprecated
    deprecationReason
  }
  inputFields {
    ...InputValue
  }
  interfaces {
    ...TypeRef
  }
  enumValues(includeDeprecated: true) {
    name
    description
    isDeprecated
    deprecationReason
  }
  possibleTypes {
    ...TypeRef
  }
}
fragment InputValue on __InputValue {
  name
  description
  type {
    ...TypeRef
  }
  defaultValue
}
fragment TypeRef on __Type {
  kind
  name
  ofType {
    kind
    name
    ofType {
      kind
      name
      ofType {
        kind
        name
        ofType {
          kind
          name
          ofType {
            kind
            name
            ofType {
              kind
              name
              ofType {
                kind
                name
              }
            }
          }
        }
      }
    }
  }
}
```

### Response:
```HTTP
{
  "data": {
    "__schema": {
      "queryType": {
        "name": "Query"
      },
      "mutationType": {
        "name": "Mutation"
      },
      "subscriptionType": {
        "name": "Subscription"
      },
      "types": [
        {
          "kind": "ENUM",
          "name": "__TypeKind",
          "description": "An enum describing what kind of type a given __Type is",
          "fields": null,
          "inputFields": null,
          "interfaces": null,
          "enumValues": [
            {
              "name": "SCALAR",
              "description": "Indicates this type is a scalar.",
              "isDeprecated": false,
              "deprecationReason": null
            },
            {
              "name": "OBJECT",
              "description": "Indicates this type is an object. `fields` and `interfaces` are valid fields.",
              "isDeprecated": false,
              "deprecationReason": null
            },
            {
              "name": "INTERFACE",
              "description": "Indicates this type is an interface. `fields` and `possibleTypes` are valid fields.",
              "isDeprecated": false,
              "deprecationReason": null
            },
            {
              "name": "UNION",
              "description": "Indicates this type is a union. `possibleTypes` is a valid field.",
              "isDeprecated": false,
              "deprecationReason": null
            },
          ],
          "possibleTypes": null
        }
      ]
    }
  }
}
```

### Inrospection Queries continued
```GraphQL
query InrospectionQuery {
  __schema {
    queryType {name}
    mutationType {name}
    subscriptionType { name}
    types {
      kind
      name
      fields {
        name
          args {
          name
        }
      }
    }
  }
}
```

```GraphQL
{
  "data": {
    "__schema": {
      "queryType": {
        "name": "Query"
      },
      "mutationType": null,
      "subscriptionType": null,
      "types": [
        {
          "kind": "OBJECT",
          "name": "Query",
          "fields": [
            {
              "name": "users",
              "args": []
            }
          ]
        },
        {
          "kind": "OBJECT",
          "name": "UserObject",
          "fields": [
            {
              "name": "id",
              "args": []
            },
            {
              "name": "username",
              "args": []
            },
            {
              "name": "first_name",
              "args": []
            },
            {
              "name": "last_name",
              "args": []
            },
            {
              "name": "state",
              "args": []
            },
            {
              "name": "email",
              "args": []
            },
            {
              "name": "history",
              "args": []
            }
          ]
        },
        {
          "kind": "SCALAR",
          "name": "ID",
          "fields": null
        },
        {
          "kind": "SCALAR",
          "name": "String",
          "fields": null
        },
        {
          "kind": "OBJECT",
          "name": "HistoryObject",
          "fields": [
            {
              "name": "id",
              "args": []
            },
            {
              "name": "last_login_timestamp",
              "args": []
            }
          ]
        },
        {
          "kind": "OBJECT",
          "name": "__Schema",
          "fields": [
            {
              "name": "types",
              "args": []
            },
            {
              "name": "queryType",
              "args": []
            },
            {
              "name": "mutationType",
              "args": []
            },
            {
              "name": "subscriptionType",
              "args": []
            },
            {
              "name": "directives",
              "args": []
            }
          ]
        },
        {
          "kind": "OBJECT",
          "name": "__Type",
          "fields": [
            {
              "name": "kind",
              "args": []
            },
            {
              "name": "name",
              "args": []
            },
            {
              "name": "description",
              "args": []
            },
            {
              "name": "fields",
              "args": [
                {
                  "name": "includeDeprecated"
                }
              ]
            },
            {
              "name": "interfaces",
              "args": []
            },
            {
              "name": "possibleTypes",
              "args": []
            },
            {
              "name": "enumValues",
              "args": [
                {
                  "name": "includeDeprecated"
                }
              ]
            },
            {
              "name": "inputFields",
              "args": []
            },
            {
              "name": "ofType",
              "args": []
            }
          ]
        },
        {
          "kind": "ENUM",
          "name": "__TypeKind",
          "fields": null
        },
        {
          "kind": "SCALAR",
          "name": "Boolean",
          "fields": null
        },
        {
          "kind": "OBJECT",
          "name": "__Field",
          "fields": [
            {
              "name": "name",
              "args": []
            },
            {
              "name": "description",
              "args": []
            },
            {
              "name": "args",
              "args": []
            },
            {
              "name": "type",
              "args": []
            },
            {
              "name": "isDeprecated",
              "args": []
            },
            {
              "name": "deprecationReason",
              "args": []
            }
          ]
        },
        {
          "kind": "OBJECT",
          "name": "__InputValue",
          "fields": [
            {
              "name": "name",
              "args": []
            },
            {
              "name": "description",
              "args": []
            },
            {
              "name": "type",
              "args": []
            },
            {
              "name": "defaultValue",
              "args": []
            }
          ]
        },
        {
          "kind": "OBJECT",
          "name": "__EnumValue",
          "fields": [
            {
              "name": "name",
              "args": []
            },
            {
              "name": "description",
              "args": []
            },
            {
              "name": "isDeprecated",
              "args": []
            },
            {
              "name": "deprecationReason",
              "args": []
            }
          ]
        },
        {
          "kind": "OBJECT",
          "name": "__Directive",
          "fields": [
            {
              "name": "name",
              "args": []
            },
            {
              "name": "description",
              "args": []
            },
            {
              "name": "locations",
              "args": []
            },
            {
              "name": "args",
              "args": []
            }
          ]
        },
        {
          "kind": "ENUM",
          "name": "__DirectiveLocation",
          "fields": null
        }
      ]
    }
  }
}

```

### GraphQL Hacking Tools
- https://github.com/dolevf/Black-Hat-GraphQL
- https://github.com/dolevf/graphw00f
- https://github.com/nikitastupin/clairvoyance/tree/main
- https://github.com/dolevf/graphql-cop
- https://github.com/commixproject/commix
- https://gitlab.com/dee-see/graphql-path-enum

