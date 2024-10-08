﻿from flask_app.constants import REQUIRED_FIELDS_TRANSACTION


def validate_field_json(data):
    """Проверяет словарь на наличие всех ключей по образцу."""
    errors = []
    for field in REQUIRED_FIELDS_TRANSACTION:
        if isinstance(field, dict):
            for key, nested_fields in field.items():
                if key not in data:
                    errors.append(f"Отсутствует поле '{key}'.")
                else:
                    if key in ["Discounts", "Invoice"] and not data[key]:
                        # Пропускаем валидацию, если Discounts или Invoice пустые
                        continue
                    elif key == "Invoice" and data[key]:
                        for nested_field in nested_fields:
                            if not nested_field in data[key].keys():
                                errors.append(
                                    f"Отсутствует поле '{nested_field}' в '{key}'."
                                )
                    else:
                        for nested_field in nested_fields:
                            if not all(nested_field in item for item in data[key]):
                                errors.append(
                                    f"Отсутствует поле '{nested_field}' в '{key}'."
                                )
        elif field not in data:
            errors.append(f"Отсутствует поле '{field}'.")
    return errors
