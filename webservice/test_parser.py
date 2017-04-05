import scangitstars


def test_parse_page():
    page = """<html>
    <body>
    <a href="/hughperkins/cltorch/stargazers">
    <svg aria-label="star" />
    123
    </a>

    <a href="/hughperkins/bar/stargazers">
    <svg aria-label="star" />
    125
    </a>

    <a href="/hughperkins/third/stargazers" aria-label="Stargazers">
    129
    </a>

    </body>
    </html>
    """
    res, nodes_found = scangitstars.parse_page(page)
    print('res', res)
    assert len(res) == 3
    assert res['cltorch'] == 123
    assert res['bar'] == 125
    assert res['third'] == 129
