# Create User
CREATE_USER = '''mutation InsertUser($name: String, $initials: String, $email: String!, $passwordHash: String!, $confirmationKey: String!) {
    insert_user(objects: {email: $email, password_hash: $passwordHash, confirmation_key: $confirmationKey, name: $name, initials: $initials}) {
        returning {
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
        }
    }
}
'''
# Update User

# Delete User


# Create Seller
CREATE_SELLER = '''mutation CreateSeller($user_uuid: uuid!, $email: String, $initials: String, $name: String) {
    insert_seller(objects: {user_uuid: $user_uuid, email: $email, initials: $initials, name: $name}) {
      returning {
        uuid
        user_uuid
        name
        is_active
        email
        created_at
      }
    }
}
'''

SET_USER_EMAIL_CONFIRMED = '''mutation SetUserEmailConfirmed($uuid: uuid) {
  __typename
  update_user(where: {uuid: {_eq: $uuid}}, _set: {has_confirmed: true}) {
    returning {
      uuid
    }
  }
}'''
