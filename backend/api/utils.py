import io

from django.http.response import FileResponse
from reportlab.lib.units import cm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas
from rest_framework import status
from rest_framework.response import Response

from recipes.models import IngredientRecipe


def create_ingredients(recipe, ingredients):
    for ingredient in ingredients:
        IngredientRecipe.objects.create(
            recipe=recipe,
            ingredient=(ingredient.get('ingredient'))['id'],
            amount=ingredient.get('amount')
        )


def prepare_ingredients_list(ingredients):
    shopping_list = []
    for item in ingredients:
        name = item.get('ingredient__name', 'Не указано')
        measurement_unit = (
            item.get('ingredient__measurement_unit', 'г.'))
        amount = item.get('ingredient_amount', 0)
        shopping_list.append(
            f'\n{name.capitalize()} - {amount}{measurement_unit}\n'
        )
    return ' '.join(shopping_list)


def _create_related_object(pk, request, serializer_class):
    serializer = serializer_class(
        data={
            'user': request.user.id,
            'recipe': pk},
        context={'request': request}
    )
    serializer.is_valid(raise_exception=True)
    serializer.save()
    return Response(serializer.data, status=status.HTTP_201_CREATED)


def _delete_related_object(pk, request, model):
    if not model.objects.filter(user=request.user, recipe=pk).exists():
        return Response(status=status.HTTP_400_BAD_REQUEST,
                        data={'message': 'Запрашиваемый объект не найден'})
    model.objects.filter(user=request.user, recipe=pk).delete()
    return Response(status=status.HTTP_204_NO_CONTENT)


def draw_pdf_report(items):
    """Рисуем отчёт о предстоящих покупках в виде PDF-файла."""
    buffer = io.BytesIO()
    # ТУТ ДОДЕЛАТЬ, ЧТОБЫ В НУЖНОЕ МЕСТО СОХРАНЯЛОСЬ
    p = canvas.Canvas('1.pdf')
    pdfmetrics.registerFont(TTFont('FreeSans', 'static/FreeSans.ttf'))
    p.setFont('FreeSans', 14)
    p.drawCentredString(
        300, 800,
        'Ваш список покупок:')
    text_object = p.beginText(2 * cm, 29.7 * cm - 2 * cm)
    for line in prepare_ingredients_list(items).splitlines(False):
        text_object.textLine(line.rstrip())
    p.drawText(text_object)
    p.showPage()
    p.save()
    buffer.seek(0)
    return FileResponse(buffer, as_attachment=True,
                        filename='shopping_list.pdf')
