# OWASP A02:2021 – Cryptographic Failures. This lab will demonstrate:

	Hardcoded cryptographic keys

	Use of weak encryption algorithms (e.g., ECB mode)

	Improper implementation of cryptographic protocols

# Objectives
## Participants will:

    Understand the risks associated with hardcoded keys and weak encryption algorithms.

    Learn how improper cryptographic implementations can be exploited.

    Practice identifying and mitigating cryptographic vulnerabilities.

# Application Features
    User Authentication: Users can log in with predefined credentials.

    Session Management: Upon successful login, a session token is generated using AES encryption in ECB mode with a hardcoded key.

    Dashboard Access: Authenticated users can access a dashboard displaying their username.

# Exploitation Guide
## Observing the Vulnerabilities
    Hardcoded Key: The AES key is hardcoded in the source code, making it accessible to anyone with access to the codebase.

    ECB Mode: Using AES in ECB mode is insecure because identical plaintext blocks result in identical ciphertext blocks, revealing patterns.

    Improper Implementation: The application lacks proper session management and does not use secure cookies or session expiration.

# Exploiting the Vulnerabilities
## Intercept the Session Cookie:

    After logging in, inspect the browser's cookies to find the session cookie.

## Decrypt the Session Token:

    Use the hardcoded key and knowledge of ECB mode to decrypt the session token and retrieve the username.

## Modify the Session Token:

    Encrypt a different username (e.g., admin) using the same method and replace the session cookie with the new token to impersonate another user.