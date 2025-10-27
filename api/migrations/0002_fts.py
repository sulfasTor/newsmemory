from django.db import migrations

SQL = """
CREATE VIRTUAL TABLE IF NOT EXISTS article_fts
USING fts5(title, content, summary, article_id UNINDEXED, content='',
           tokenize='porter');

CREATE TRIGGER IF NOT EXISTS article_ai AFTER INSERT ON api_article BEGIN
  INSERT INTO article_fts(rowid, title, content, summary, article_id)
  VALUES (new.rowid, new.title, new.content, new.summary, new.id);
END;

CREATE TRIGGER IF NOT EXISTS article_ad AFTER DELETE ON api_article BEGIN
  INSERT INTO article_fts(article_fts, rowid, title, content, summary, article_id)
  VALUES ('delete', old.rowid, old.title, old.content, old.summary, old.id);
END;

CREATE TRIGGER IF NOT EXISTS article_au AFTER UPDATE ON api_article BEGIN
  INSERT INTO article_fts(article_fts, rowid, title, content, summary, article_id)
  VALUES ('delete', old.rowid, old.title, old.content, old.summary, old.id);
  INSERT INTO article_fts(rowid, title, content, summary, article_id)
  VALUES (new.rowid, new.title, new.content, new.summary, new.id);
END;
"""

class Migration(migrations.Migration):
    dependencies = [('api','0001_initial')]
    operations = [migrations.RunSQL(SQL)]
