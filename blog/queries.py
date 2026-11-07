"""Queries behind the views. Part 2 of the lab happens in this file."""
from blog.models import Post


def posts_for_front_page():
    # `author` is a ForeignKey (one author per post): select_related joins it in the
    # same query. `tags` is many-to-many: prefetch_related runs one extra query for
    # all the tags of all the posts. Total: 2 queries, no matter how many posts.
    return (
        Post.objects.filter(published=True)
        .select_related("author")
        .prefetch_related("tags")
        .order_by("-published_at")
    )
