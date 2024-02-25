
curl -X GET http://localhost:8000/api/user/me -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyU2VxIjoxLCJpYXQiOjE3MDg4NDY2MDUsImV4cCI6MTcwODkzMzAwNX0.hVep0CYUmN-CN5djVoGPQf-YqVABjlHfqXEVDeRhAiY"
curl -X PUT http://localhost:8000/api/user/update -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyU2VxIjoxLCJpYXQiOjE3MDg4NDY2MDUsImV4cCI6MTcwODkzMzAwNX0.hVep0CYUmN-CN5djVoGPQf-YqVABjlHfqXEVDeRhAiY" -H "Content-Type: application/json" -d '{"userName": "dany"}'
