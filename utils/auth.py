def create_verification_link(base_url: str, token: str) -> str:
    return f"{base_url}/verify?token={token}"
