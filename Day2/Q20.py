codes = [200, 201, 404, 500, 301, 403, 502, 204]

result = [(code,
           "success" if 200 <= code < 300 else
           "redirect" if 300 <= code < 400 else
           "client_error" if 400 <= code < 500 else
           "server_error")
          for code in codes]

print(result)