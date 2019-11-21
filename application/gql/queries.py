# Get User (by email)
GET_USER_BY_EMAIL = '''query GetUserByEmail($email: String!) {
  user(where: {email: {_eq: $email}}) {
    uuid
    id
    created_at
    updated_at
    email
    password_hash
    role
    confirmation_key
    has_confirmed
  }
}'''
# Get User (by uuid)
GET_USER_BY_UUID = '''query GetUserByUUID($uuid: String!) {
  user(where: {uuid: {_eq: $uuid}}) {
    uuid
    id
    created_at
    updated_at
    email
    password_hash
    role
    confirmation_key
    has_confirmed
  }
}'''
# Get Session (by user id)