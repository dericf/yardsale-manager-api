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
    token_version
    name
    initials
    password_reset_code
    has_completed_onboarding
  }
}'''
# Get User (by uuid)
GET_USER_BY_UUID = '''query GetUserByUUID($uuid: uuid!) {
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
    token_version
    name
    initials
    password_reset_code
    has_completed_onboarding
  }
}'''
# Get Session (by user id)


#
# GET all yardsales
#
GET_PUBLIC_YARDSALES = '''query GetPublicYardsales {
  yardsale(where: {is_public: {_eq: true}}) {
    uuid
    name
    email
    pos_lat
    pos_lng
    address_text
  }
}'''