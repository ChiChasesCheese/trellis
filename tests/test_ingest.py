"""Ingest: a corpus becomes sections and an outline, whatever its format."""

import json
import zipfile
from pathlib import Path

import pytest

from trellis.clippings import ClipError, FetchedPage
from trellis.corpus import CorpusError, load_corpus, load_outline
from trellis.ingest import extract_markdown, html_to_markdown, ingest


def test_html_to_markdown_keeps_structure():
    html = """<html><head><title>x</title><style>p{}</style></head><body>
    <h2 class="t"><span>3.4 生产者配置</span></h2>
    <p>acks 指定了 <b>多少个</b> 副本。<code>acks=all</code> 最安全。</p>
    <ul><li>一</li><li>二</li></ul>
    <pre><code>props.put("acks", "all");
send();</code></pre>
    <table><tr><th>参数</th><th>默认</th></tr><tr><td>acks</td><td>1</td></tr></table>
    <p>见 <a href="https://kafka.apache.org/">官网</a> 和 <a href="#nav_1">内部锚点</a>。</p>
    </body></html>"""
    md = html_to_markdown(html)
    assert "## 3.4 生产者配置" in md
    assert "**多少个**" in md and "`acks=all`" in md
    assert "- 一\n- 二" in md
    assert '```\nprops.put("acks", "all");\nsend();\n```' in md
    assert "| 参数 | 默认 |\n|---|---|\n| acks | 1 |" in md
    assert "[官网](https://kafka.apache.org/)" in md and "内部锚点" in md
    assert "p{}" not in md and "x" not in md.split("\n")[0]


def _epub(path: Path) -> Path:
    """A two-chapter EPUB 2 with an NCX: chapter 2 has a sub-heading in the
    same file and a continuation file the nav never names."""
    pages = {
        "title.xhtml": "<html><body><h1>Title page</h1></body></html>",
        "ch1.xhtml": "<html><body><h1>第1章 初识</h1><p>什么是 Kafka。</p></body></html>",
        "ch2.xhtml": "<html><body><h1>第2章 生产者</h1><p>概览。</p>"
                     "<h2 id='s21'>2.1 acks</h2><p>acks 的三个值。</p></body></html>",
        "ch2b.xhtml": "<html><body><p>2.1 的续篇。</p></body></html>",
    }
    manifest = "".join(
        f'<item id="{n.split(".")[0]}" href="{n}" media-type="application/xhtml+xml"/>'
        for n in pages)
    opf = f"""<?xml version="1.0"?>
<package xmlns="http://www.idpf.org/2007/opf" version="2.0" unique-identifier="u">
 <metadata xmlns:dc="http://purl.org/dc/elements/1.1/"><dc:title>测试书</dc:title></metadata>
 <manifest>{manifest}<item id="ncx" href="toc.ncx" media-type="application/x-dtbncx+xml"/></manifest>
 <spine toc="ncx"><itemref idref="title"/><itemref idref="ch1"/><itemref idref="ch2"/><itemref idref="ch2b"/></spine>
</package>"""
    ncx = """<?xml version="1.0"?>
<ncx xmlns="http://www.daisy.org/z3986/2005/ncx/" version="2005-1"><navMap>
 <navPoint id="a"><navLabel><text>第1章 初识</text></navLabel><content src="ch1.xhtml"/></navPoint>
 <navPoint id="b"><navLabel><text>第2章 生产者</text></navLabel><content src="ch2.xhtml"/>
   <navPoint id="c"><navLabel><text>2.1 acks</text></navLabel><content src="ch2.xhtml#s21"/></navPoint>
 </navPoint>
</navMap></ncx>"""
    with zipfile.ZipFile(path, "w") as z:
        z.writestr("mimetype", "application/epub+zip")
        z.writestr("META-INF/container.xml",
                   '<container xmlns="urn:oasis:names:tc:opendocument:xmlns:container">'
                   '<rootfiles><rootfile full-path="OEBPS/content.opf"/></rootfiles></container>')
        z.writestr("OEBPS/content.opf", opf)
        z.writestr("OEBPS/toc.ncx", ncx)
        for name, html in pages.items():
            z.writestr(f"OEBPS/{name}", html)
    return path


def _declare(root: Path, corpus_id: str, **fields) -> Path:
    import yaml
    (root / "corpora").mkdir(exist_ok=True)
    path = root / "corpora" / f"{corpus_id}.yaml"
    path.write_text(yaml.safe_dump(fields, allow_unicode=True), encoding="utf-8")
    return path


def test_epub_sections_follow_the_table_of_contents(tmp_path):
    book = _epub(tmp_path / "book.epub")
    corpus = load_corpus(_declare(tmp_path, "test-book", title="测试书", license="commercial",
                                  domain="demo", lang="zh", file=str(book)))
    result = ingest(corpus, tmp_path)
    outline = load_outline(corpus.outline_path(tmp_path))
    assert outline.title == "测试书"
    assert [s.title for s in outline.sections] == ["第1章 初识", "第2章 生产者"]
    assert outline.sections[1].children == ["2.1 acks"]
    # A commercial book's text lands in the gitignored local dir, never the archive.
    text_dir = tmp_path / "sources" / "local" / "test-book"
    assert text_dir.exists() and not (tmp_path / "sources" / "archive").exists()
    ch2 = (text_dir / f"{outline.sections[1].id}.md").read_text(encoding="utf-8")
    assert "## 2.1 acks" in ch2 and "2.1 的续篇" in ch2, "continuation file folds into its chapter"
    assert "Title page" not in ch2 and not result.notes


def test_markdown_splits_at_headings(tmp_path):
    src = tmp_path / "notes.md"
    src.write_text("# One\n\nalpha\n\n## One point one\n\nbeta\n\n# Two\n\ngamma\n", encoding="utf-8")
    outline, notes = extract_markdown(src, "notes")
    assert [s.title for s in outline.sections] == ["One", "Two"]
    assert outline.sections[0].children == ["One point one"]
    assert "beta" in outline.sections[0].text and "gamma" in outline.sections[1].text


def test_web_chapters_checkpoint_and_resume(tmp_path):
    urls = ["https://ex.org/b/one.html", "https://ex.org/b/two.html"]
    corpus = load_corpus(_declare(tmp_path, "free", title="Free", license="free-online",
                                  domain="demo", chapters=urls))
    calls: list[str] = []

    def flaky(url):
        calls.append(url)
        if url.endswith("two.html") and calls.count(url) == 1:
            raise ClipError("boom")
        return FetchedPage(title=url.rsplit("/", 1)[-1], markdown="prose " * 50)

    first = ingest(corpus, tmp_path, fetch=flaky)
    assert [s.id for s in first.outline.sections] == ["01-one"]
    assert any("FAILED" in n for n in first.notes)
    state = json.loads((tmp_path / "pipeline/state/ingest-free.json").read_text())
    assert state["corpus"] == "free" and state["chapters"][urls[1]]["status"] == "failed"
    # Without --retry the failure stays; with it the chapter lands, and the
    # done chapter is not fetched again.
    assert len(ingest(corpus, tmp_path, fetch=flaky).outline.sections) == 1
    second = ingest(corpus, tmp_path, retry=True, fetch=flaky)
    assert [s.id for s in second.outline.sections] == ["01-one", "02-two"]
    assert calls.count(urls[0]) == 1
    assert (tmp_path / "sources" / "archive" / "free" / "02-two.md").exists()


def test_declaration_is_checked(tmp_path):
    with pytest.raises(CorpusError, match="exactly one of"):
        load_corpus(_declare(tmp_path, "bad", title="x", license="cc-by", domain="d"))
    with pytest.raises(CorpusError, match="freely licensed"):
        load_corpus(_declare(tmp_path, "paid", title="x", license="commercial", domain="d",
                             chapters=["https://x"]))
    with pytest.raises(CorpusError, match="license"):
        load_corpus(_declare(tmp_path, "lic", title="x", license="stolen", domain="d", file="a.epub"))
