"""YOUR answers. One function per question, no arguments.

Write the ORM query that answers each question and return it (a QuerySet or a
list). Do not write SQL and do not filter in Python what the database can
filter. Check yourself with:

    python manage.py duel                 # all of them
    python manage.py duel --question q4   # just one

Question 5 asks for two numbers per post: annotate them as `n_comments` and
`n_tags`.
"""
from datetime import date

from django.db.models import Count

from blog.models import Author, Comment, Post


def q1():
    """Los artículos que ya están publicados."""
    return Post.objects.filter(published=True)


def q2():
    """Los artículos que no tienen categoría asignada."""
    return Post.objects.filter(category__isnull=True)


def q3():
    """Los artículos publicados entre el 1 de marzo y el 31 de mayo de 2026, ambos días incluidos."""
    # `range` is BETWEEN: both ends are inclusive (gt/lt would drop the two boundary posts).
    return Post.objects.filter(published_at__range=(date(2026, 3, 1), date(2026, 5, 31)))


def q4():
    """Los artículos con más de dos comentarios."""
    # One query: the count is computed by the database, not one `.count()` per post.
    return Post.objects.annotate(n_comments=Count("comments")).filter(n_comments__gt=2)


def q5():
    """Los tres artículos publicados con más comentarios; de cada uno, cuántos comentarios
    (`n_comments`) y cuántas etiquetas (`n_tags`)."""
    # Two joins multiply the rows (comments x tags), so each Count needs distinct=True.
    return (
        Post.objects.filter(published=True)
        .annotate(
            n_comments=Count("comments", distinct=True),
            n_tags=Count("tags", distinct=True),
        )
        .order_by("-n_comments")[:3]
    )


def q6():
    """Los artículos escritos por autores de Perú (publicados o no)."""
    # The country lives in Profile (one to one), so the path goes author -> profile -> country.
    return Post.objects.filter(author__profile__country="Perú")


def q7():
    """Los comentarios de los artículos de la categoría «Tecnología»."""
    return Comment.objects.filter(post__category__name="Tecnología")


def q8():
    """Los autores que nunca han publicado un artículo."""
    # exclude() over a multi-valued relation builds a NOT IN subquery: it keeps authors
    # with no posts at all (Diego) and authors with only drafts (Carla).
    return Author.objects.exclude(posts__published=True)
