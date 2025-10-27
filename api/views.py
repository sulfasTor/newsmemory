from django.db import connection
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import Article, ArticleLink, Entity, Reading, Source, Tag
from .serializers import (
    ArticleLinkSerializer,
    ArticleSerializer,
    EntitySerializer,
    ReadingSerializer,
    SourceSerializer,
    TagSerializer,
)


class SourceViewSet(viewsets.ModelViewSet):
    queryset = Source.objects.all().order_by("name")
    serializer_class = SourceSerializer


class TagViewSet(viewsets.ModelViewSet):
    queryset = Tag.objects.all().order_by("name")
    serializer_class = TagSerializer


class EntityViewSet(viewsets.ModelViewSet):
    queryset = Entity.objects.all().order_by("name")
    serializer_class = EntitySerializer


class ArticleViewSet(viewsets.ModelViewSet):
    queryset = (
        Article.objects.select_related("source")
        .prefetch_related("tags")
        .order_by("-published_at", "-created_at")
    )
    serializer_class = ArticleSerializer

    @action(detail=False, methods=["get"])
    def search(self, request):
        q = request.query_params.get("q", "")
        if not q:
            return Response({"results": []})
        with connection.cursor() as cur:
            cur.execute(
                """
                SELECT a.id, a.title, a.url, a.published_at
                FROM article_fts f
                JOIN core_article a ON a.rowid = f.rowid
                WHERE article_fts MATCH ?
                ORDER BY rank
                LIMIT 50
            """,
                [q],
            )
            rows = cur.fetchall()
        results = [{"id": r[0], "title": r[1], "url": r[2], "published_at": r[3]} for r in rows]
        return Response({"results": results})


class ReadingViewSet(viewsets.ModelViewSet):
    queryset = Reading.objects.select_related("article").order_by("-created_at")
    serializer_class = ReadingSerializer


class ArticleLinkViewSet(viewsets.ModelViewSet):
    queryset = ArticleLink.objects.all()
    serializer_class = ArticleLinkSerializer
