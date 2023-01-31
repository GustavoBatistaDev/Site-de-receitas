from recipes.models import Recipe


def verify_slug(recipe):
    recipe = Recipe.objects.filter(slug=recipe.slug)
    if recipe:
        return True
    return False
