
curl -X GET http://localhost:8000/api/user/me -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyU2VxIjozLCJpYXQiOjE3MDg4NTgxMDEsImV4cCI6MTcwODk0NDUwMX0.ndvBiNFkO4bZFl0zST2odfV05Bebo5Mm63J5Q1jfB-g"
curl -X PUT http://localhost:8000/api/user/update -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyU2VxIjozLCJpYXQiOjE3MDg4NTgxMDEsImV4cCI6MTcwODk0NDUwMX0.ndvBiNFkO4bZFl0zST2odfV05Bebo5Mm63J5Q1jfB-g" -H "Content-Type: application/json" -d '{"userName": "dany"}'
curl -X GET http://localhost:8000/api/point/me -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyU2VxIjozLCJpYXQiOjE3MDg4NTgxMDEsImV4cCI6MTcwODk0NDUwMX0.ndvBiNFkO4bZFl0zST2odfV05Bebo5Mm63J5Q1jfB-g" 
