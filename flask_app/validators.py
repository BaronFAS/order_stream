from flask_app.constants import REQUIRED_FIELDS_TRANSACTION as RFT


def validate_field(data):
    """Проверяет словарь на наличие всех ключей по образцу."""
    errors = []
    for field in RFT:
        if isinstance(field, dict):
            for key, nested_fields in field.items():
                if key not in data:
                    errors.append(f"Отсутствует поле '{key}'.")
                else:
                    for nested_field in nested_fields:
                        if not all(nested_field in item for item in data[key]):
                            errors.append(
                                f"Отсутствует поле '{nested_field}' в '{key}'."
                            )
        elif field not in data:
            errors.append(f"Отсутствует поле '{field}'.")
    return errors
