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
  update_user(where: {uuid: {_eq: $uuid}}, _set: {has_confirmed: true}) {
    returning {
      uuid
    }
  }
}'''

SET_PASSWORD_RESET_CODE = '''mutation SetPasswordResetCode($uuid: uuid!, $code: String!) {
  update_user(where: {uuid: {_eq: $uuid}}, _set: {password_reset_code: $code}) {
    returning {
      uuid
    }
  }
}'''


UPDATE_PASSWORD = '''mutation UpdatePasswordAndClearResetCode($uuid: uuid!, $password: String!) {
  update_user(where: {uuid: {_eq: $uuid}}, _set: {password_reset_code: null, password_hash: $password}) {
    returning {
      uuid
    }
  }
}'''
