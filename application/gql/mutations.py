# Create User
CREATE_USER = '''mutation InsertUser($email: String!, $passwordHash: String!, $confirmationKey: String!) {
    insert_user(objects: {email: $email, password_hash: $passwordHash, confirmation_key: $confirmationKey}) {
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
        }
    }
}

'''
# Update User

# Delete User
