class AppError(Exception):
    def __init__(self, message: str, status_code: int):
        super().__init__(message)
        self.message = message
        self.status_code = status_code


class BadRequestError(AppError):
    def __init__(self, message="Solicitud incorrecta"):
        super().__init__(message, status_code=400)


class ForbiddenError(AppError):
    def __init__(self, message="Acción no permitida"):
        super().__init__(message, status_code=403)


class NotFoundError(AppError):
    def __init__(self, message="Entidad no encontrada"):
        super().__init__(message, status_code=404)


class ConflictError(AppError):
    def __init__(self, message="Conflicto con un registro existente"):
        super().__init__(message, status_code=409)