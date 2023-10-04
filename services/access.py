import uuid


def get_access(unit: str) -> str:
    code = None
    match unit:
        case 'manager':
            code = uuid.uuid4().hex
        case 'master':
            code = uuid.uuid4().hex
        case 'staff':
            code = uuid.uuid4().hex
    return code
