import uuid

from django.db import models


class TimeStamped(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Source(TimeStamped):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=200, unique=True)
    homepage = models.URLField(blank=True)
    rss = models.URLField(blank=True)
    country = models.CharField(max_length=64, blank=True)
    language = models.CharField(max_length=16, blank=True)

    def __str__(self):
        return self.name


class Tag(TimeStamped):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.SlugField(max_length=64, unique=True)

    def __str__(self):
        return self.name


class Article(TimeStamped):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    source = models.ForeignKey(Source, on_delete=models.PROTECT, related_name="articles")
    url = models.URLField(unique=True)
    title = models.CharField(max_length=500, db_index=True)
    published_at = models.DateTimeField(null=True, blank=True, db_index=True)
    byline = models.CharField(max_length=300, blank=True)
    language = models.CharField(max_length=16, blank=True)
    summary = models.TextField(blank=True)
    content = models.TextField(blank=True)  # full text if you store it
    tags = models.ManyToManyField(Tag, blank=True, related_name="articles")

    class Meta:
        indexes = [
            models.Index(fields=["published_at"]),
            models.Index(fields=["title"]),
        ]


class Entity(TimeStamped):
    """Named entity for later correlation (people/orgs/places/etc.)."""

    PERSON, ORG, GPE, EVENT, WORK, OTHER = "PERSON", "ORG", "GPE", "EVENT", "WORK", "OTHER"
    TYPES = [
        (PERSON, "PERSON"),
        (ORG, "ORG"),
        (GPE, "GPE"),
        (EVENT, "EVENT"),
        (WORK, "WORK"),
        (OTHER, "OTHER"),
    ]
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255, db_index=True)
    type = models.CharField(max_length=12, choices=TYPES, default=OTHER)

    class Meta:
        unique_together = [("name", "type")]


class ArticleEntity(models.Model):
    """Bridge with extra fields to score salience for later ML."""

    article = models.ForeignKey(Article, on_delete=models.CASCADE, related_name="article_entities")
    entity = models.ForeignKey(Entity, on_delete=models.CASCADE, related_name="mentions")
    count = models.PositiveIntegerField(default=1)
    salience = models.FloatField(default=0.0)

    class Meta:
        unique_together = [("article", "entity")]


class Reading(TimeStamped):
    """Your interaction: read/archived/notes/rating."""

    TO_READ, READING, READ, ARCHIVED = "to_read", "reading", "read", "archived"
    STATES = [(TO_READ, "to_read"), (READING, "reading"), (READ, "read"), (ARCHIVED, "archived")]
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    article = models.ForeignKey(Article, on_delete=models.CASCADE, related_name="readings")
    state = models.CharField(max_length=16, choices=STATES, default=TO_READ, db_index=True)
    read_at = models.DateTimeField(null=True, blank=True)
    rating = models.PositiveSmallIntegerField(null=True, blank=True)  # 1..5
    notes = models.TextField(blank=True)


# Optional: lightweight relation between articles (dedup/cluster)
class ArticleLink(TimeStamped):
    FROM_REF, CITATION, UPDATE, DUPLICATE, SAME_STORY = (
        "ref",
        "citation",
        "update",
        "duplicate",
        "same_story",
    )
    TYPES = [
        (FROM_REF, "ref"),
        (CITATION, "citation"),
        (UPDATE, "update"),
        (DUPLICATE, "duplicate"),
        (SAME_STORY, "same_story"),
    ]
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    src = models.ForeignKey(Article, on_delete=models.CASCADE, related_name="out_links")
    dst = models.ForeignKey(Article, on_delete=models.CASCADE, related_name="in_links")
    kind = models.CharField(max_length=16, choices=TYPES, default=SAME_STORY)

    class Meta:
        unique_together = [("src", "dst", "kind")]
