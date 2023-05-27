1. Notice the message in the console about Graphql
2. Query the graphql endpoint and notice the `flagnn` element
3. Query the flag element values until you find the flag `curl 'http://localhost:4000/graphql' -H 'Content-Type: application/json' --data-binary '{"query":"{\n  flag86\n}","variables":{}}'`