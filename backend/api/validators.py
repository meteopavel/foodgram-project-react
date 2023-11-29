from rest_framework.exceptions import ValidationError

from googletrans import Translator

translator = Translator()


def validate_empty_fields(validated_data):
    required_fields = ('tags', 'ingredients')
    for field in required_fields:
        if field not in validated_data.keys():
            raise ValidationError(f"Требуется поле {field}")


def validate_list(value, field):
    translation = translator.translate(
        field.replace('validate_', ''), dest="ru"
    )
    if len(value) == 0:
        raise ValidationError(f"Нужно добавить {translation.text}!")
    elif len(set(value)) != len(value):
        raise ValidationError(f"Нельзя дублировать {translation.text}!")
